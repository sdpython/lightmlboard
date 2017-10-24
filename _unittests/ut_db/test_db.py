#-*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest


try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import ExtTestCase, get_temp_folder
from src.lightmlboard.dbmanager import DatabaseCompetition


class TestDb(ExtTestCase):

    def test_creation_memory(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        db = DatabaseCompetition(":memory:")
        db.connect()
        dbl = db.get_table_list()
        db.close()
        self.assertEqual(
            dbl, ['competitions', 'players', 'submissions', 'teams'])

    def test_creation_file(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

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
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        db = DatabaseCompetition(":memory:")
        data = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        opt = os.path.join(data, "ex_default_options.py")
        db.init_from_options(opt)
        db.connect()
        dft = db.to_df("teams")
        dfp = db.to_df("players")
        db.close()
        self.assertEqual(dft.shape, (1, 2))
        self.assertEqual(dft.iloc[0, 1], "team1")
        self.assertEqual(dfp.shape, (1, 7))


if __name__ == "__main__":
    unittest.main()
