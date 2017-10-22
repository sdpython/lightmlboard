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
from pyquickhelper.pycode import ExtTestCase
from src.lightmlboard.competition import Competition


class TestMetrics(ExtTestCase):

    def test_mse(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        compet = Competition("/compet", "compet1",
                             "description", "mse", [[0, 1, 2]])
        res = compet.evaluate([[0, 1, 2]])
        self.assertEqual(res, {'mse': 0.0})
        res = compet.evaluate([[0, 4, 2]])
        self.assertEqual(res, {'mse': 3.0})

    def test_mean_squared_error(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        compet = Competition("/compet", "compet1",
                             "description", "mean_squared_error", [[0, 1, 2]])
        res = compet.evaluate([[0, 1, 2]])
        self.assertEqual(res, {'mean_squared_error': 0.0})
        res = compet.evaluate([[0, 4, 2]])
        self.assertEqual(res, {'mean_squared_error': 3.0})


if __name__ == "__main__":
    unittest.main()
