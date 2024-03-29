# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""
import os
import unittest
from io import StringIO
import pandas
from pyquickhelper.pycode import ExtTestCase, get_temp_folder
from lightmlboard.dbmanager import DatabaseCompetition
from lightmlboard.competition import Competition


class TestDb(ExtTestCase):

    def test_creation_memory(self):
        db = DatabaseCompetition(":memory:")
        db.connect()
        dbl = db.get_table_list()
        db.close()
        self.assertEqual(
            dbl, ['competitions', 'players', 'submissions', 'teams'])

    def test_creation_file(self):
        temp = get_temp_folder(__file__, "temp_creation_file")
        name = os.path.join(temp, "ex.db3")
        db = DatabaseCompetition(name)
        db.connect()
        dbl = db.get_table_list()
        db.close()
        self.assertEqual(
            dbl, ['competitions', 'players', 'submissions', 'teams'])
        self.assertExists(name)

    def test_creation_db(self):
        db = DatabaseCompetition(":memory:")
        data = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        opt = os.path.join(data, "ex_default_options.py")
        db.init_from_options(opt)
        db.connect()
        dft = db.to_df("teams")
        dfp = db.to_df("players")
        dfc = db.to_df("competitions")
        dfs = db.to_df("submissions")
        db.close()
        self.assertEqual(dft.shape, (1, 2))
        self.assertEqual(dft.iloc[0, 1], "team1")  # pylint: disable=E1101
        self.assertEqual(dfp.shape, (1, 7))
        self.assertEqual(dfc.shape, (1, 7))
        self.assertEqual(dfs.shape, (1, 7))

    def test_submission(self):
        data = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        fname = os.path.join(data, "off_eval_all_Y.txt")
        df = pandas.read_csv(fname)
        pred = [0.9 if v else 0.1 for v in df.hasE]
        dfpred = pandas.DataFrame(pred, columns=["c1"])
        s = StringIO()
        dfpred.to_csv(s, index=False)
        sub = s.getvalue()

        db = DatabaseCompetition(":memory:")
        opt = os.path.join(data, "ex_default_options.py")
        db.init_from_options(opt)
        db.connect()

        cid = db.get_cpt_id()
        pid = db.get_player_id()

        db.submit(cid[0], pid[0], sub)
        db.close()

        db.connect()
        subs = list(db.execute("SELECT * FROM submissions"))
        db.close()

        self.assertEqual(len(subs), 2)
        self.assertEqual(
            subs[-1][-2:], ('mean_squared_error', 0.009999999999999997))

    def test_get_competition(self):
        db = DatabaseCompetition(":memory:")
        data = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        opt = os.path.join(data, "ex_default_options.py")
        db.init_from_options(opt)
        db.connect()
        cpt = db.get_competition(0)
        db.close()
        self.assertIsInstance(cpt, Competition)

    def test_get_results(self):
        db = DatabaseCompetition(":memory:")
        data = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        opt = os.path.join(data, "ex_default_options.py")
        db.init_from_options(opt)
        db.connect()

        data = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        fname = os.path.join(data, "off_eval_all_Y.txt")
        df = pandas.read_csv(fname)
        pred = [0.9 if v else 0.1 for v in df.hasE]
        dfpred = pandas.DataFrame(pred, columns=["c1"])
        s = StringIO()
        dfpred.to_csv(s, index=False)
        sub = s.getvalue()
        db.submit(0, 0, sub)

        df = db.get_results(0)
        db.close()
        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(df.shape, (1, 9))


if __name__ == "__main__":
    TestDb().test_creation_memory()
    unittest.main()
