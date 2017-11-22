#-*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
import numpy


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
from src.lightmlboard.metrics import l1_reg_max


class TestMetricsCustom(ExtTestCase):

    def test_l1_reg_max(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        exp = [50, 60, 100, 180, 200]
        val = [50, 60, 100, 180, 180]
        r = l1_reg_max(exp, val)
        self.assertEqual(r, 0)

        exp = [50, 60, 100, 180, 200]
        val = [50, 60, 100, 160, 180]
        r = l1_reg_max(exp, val)
        self.assertEqual(r, 0.02222222222222222)

        exp = numpy.array(exp)
        val = numpy.array(val)

        r = l1_reg_max(exp, val)
        self.assertEqual(r, 0.02222222222222222)


if __name__ == "__main__":
    unittest.main()
