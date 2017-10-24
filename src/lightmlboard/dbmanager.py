"""
@file
@brief Manages a sqlite3 database to store the results.
"""
import pandas
from .dbengine import Database
from .options_helpers import read_options, read_users


class DatabaseCompetition(Database):
    """
    Holds the data used for competitions. Tables:

    Competitions

    * cpt_id
    * cpt_name
    * metric
    * datafile
    * description

    Teams

    * team_id
    * team_name

    Players

    * player_id
    * team_id
    * player_name
    * mail
    * login
    * pwd

    Submission

    * cpt_id
    * player_id
    * date
    * filename
    * metric_value
    """

    def __init__(self, dbfile):
        """
        @param      dbfile      filename or ``:memory:``
        """
        Database.__init__(self, dbfile)
        self._init()

    def _init(self):
        """
        Creates the tables if not present.
        """
        self.connect()
        tables = self.get_table_list()
        adds = dict(competitions=DatabaseCompetition._col_competitions,
                    teams=DatabaseCompetition._col_teams,
                    players=DatabaseCompetition._col_players,
                    submissions=DatabaseCompetition._col_submissions)
        for k, v in adds.items():
            if k not in tables:
                self.create_table(k, v())
        self.commit()
        self.close()

    def init_from_options(self, filename):
        """
        Initializes the database. It skips a table if
        it exists.

        @param      filename        filename
        """
        opt = read_options(filename)
        if opt is None:
            raise ValueError("No option in '{0}'.".format(filename))
        users = read_users(opt["allowed_users"])

        if not self.has_rows("teams"):
            teams = map(lambda x: x[1]['team'], users.items())
            tdf = pandas.DataFrame({"team_name": list(teams)})
            tdf.reset_index(drop=False, inplace=True)
            tdf.columns = ["team_id", "team_name"]
            tdf.to_sql("teams", self.Connection,
                       if_exists="append", index=False)

        if not self.has_rows("players"):
            players = list(map(lambda x: x[1], users.items()))
            pdf = pandas.DataFrame(players)
            pdf.reset_index(drop=False, inplace=True)
            tdf = self.to_df("teams")
            pdf["player_name"] = pdf["name"]
            pdf["player_id"] = pdf["index"]
            pdf = pdf.merge(tdf, left_on="team", right_on="team_name")
            pdf = pdf.drop(["name", "team_name", "index", "team"], axis=1)
            pdf.to_sql("players", self.Connection,
                       if_exists="append", index=False)

    def to_df(self, table):
        """
        Returns the content of a table as a dataframe.
        """
        return pandas.read_sql("SELECT * FROM {0}".format(table), self.Connection)

    @property
    def Connection(self):
        """
        Returns the connexion.
        """
        self._check_connection()
        return self._connection

    def _col_competitions():
        return [('cpt_id', int), ('cpt_name', str), ('metric', str), ('datafile', str), ('description', str)]

    def _col_teams():
        return [('team_id', int), ('team_name', str)]

    def _col_players():
        return [('player_id', int), ('team_id', int), ('metric', str), ('player_name', str),
                ('mail', str), ('login', str), ('pwd', str)]

    def _col_submissions():
        return [('cpt_id', int), ('player_id', int), ('date', str),
                ('filename', str), ('metric_value', str)]
