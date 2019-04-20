# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from lightmlboard.competition import Competition
from lightmlboard.default_options import LightMLBoardDefaultOptions


class TestCompetition(ExtTestCase):

    def test_competition(self):
        vals = LightMLBoardDefaultOptions.competitions
        ds = [v.to_dict() for v in vals]
        vals2 = [Competition(**d) for d in ds]
        ds2 = [v.to_dict() for v in vals2]
        self.assertEqual(ds, ds2)


if __name__ == "__main__":
    unittest.main()
