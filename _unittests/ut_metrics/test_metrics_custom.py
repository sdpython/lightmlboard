# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""
import io
import unittest
import pandas
import numpy
from pyquickhelper.pycode import ExtTestCase
from lightmlboard.metrics import l1_reg_max, multi_label_jaccard


class TestMetricsCustom(ExtTestCase):

    def test_l1_reg_max(self):
        exp = [50, 60, 100, 180, 200]
        val = [50, 60, 100, 180, 180]
        r = l1_reg_max(exp, val)
        self.assertEqual(r, 0)

        exp = [50, 60, 100, 180, 200]
        val = [50, 60, 100, 160, 180]
        r = l1_reg_max(exp, val)
        self.assertEqual(r, 0.02222222222222222)
        r = l1_reg_max(exp, val, nomax=True)
        self.assertEqual(r, 0)

        exp = numpy.array(exp)
        val = numpy.array(val)

        r = l1_reg_max(exp, val)
        self.assertEqual(r, 0.02222222222222222)

        r = l1_reg_max(exp, val, nomax=True)
        self.assertEqual(r, 0)

        exp = {i: exp[i] for i in range(0, len(exp))}
        val = {i: val[i] for i in range(0, len(val))}
        r = l1_reg_max(exp, val)
        self.assertEqual(r, 0.02222222222222222)
        r = l1_reg_max(exp, val, nomax=True)
        self.assertEqual(r, 0)

        exp = [50, 60, 100, 180, 200]
        val = [50, 60, 100, 160]
        self.assertRaise(lambda: l1_reg_max(exp, val), ValueError)
        exp = numpy.array(exp)
        val = numpy.array(val)
        self.assertRaise(lambda: l1_reg_max(exp, val), ValueError)
        exp = {i: exp[i] for i in range(0, len(exp))}
        val = {i: val[i] for i in range(0, len(val))}
        self.assertRaise(lambda: l1_reg_max(exp, val), ValueError)
        self.assertRaise(lambda: l1_reg_max(exp, tuple(val)), TypeError)

    def test_l1_reg_max_streams(self):
        st1 = io.StringIO()
        st2 = io.StringIO()
        exp = [50, 60, 100, 180, 200]
        val = [50, 60, 100, 180, 180]
        d1 = pandas.DataFrame(dict(name=exp)).reset_index(drop=False)
        d2 = pandas.DataFrame(dict(name=val)).reset_index(drop=False)
        d1.to_csv(st1, index=False, header=None, sep=';')
        d2.to_csv(st2, index=False, header=None, sep=';')
        r = l1_reg_max(io.StringIO(st1.getvalue()),
                       io.StringIO(st2.getvalue()))
        self.assertEqual(r, 0)

    def test_classification_jaccard(self):
        exp = ["4", "5", "6,7", [6, 7], (6, 7), {6, 7}]
        val = ["4", ["5"], "6,7", [6, 7], (6, 7), {6, 7}]
        r = multi_label_jaccard(exp, val)
        self.assertEqual(r, 1)

        exp = ["4", "5", "6,7", [6, 7], (6, 7), {6, 7}]
        val = ["4", ["5"], "7", [7], (7,), {7}]
        r = multi_label_jaccard(exp, val)
        self.assertEqual(r, 0.6666666666666666)

        dexp = {i: exp[i] for i in range(0, len(exp))}
        dval = {i: val[i] for i in range(0, len(val))}
        r = multi_label_jaccard(dexp, dval)
        self.assertEqual(r, 0.6666666666666666)

        val = val[:-1]
        self.assertRaise(lambda: multi_label_jaccard(exp, val), ValueError)
        self.assertRaise(lambda: multi_label_jaccard(
            exp, tuple(val)), TypeError)

    def test_classification_jaccard_streams(self):
        st1 = io.StringIO()
        st2 = io.StringIO()
        exp = ["4", "5", "6,7", "6,7", "6,7", "6,7"]
        val = ["4", "5", "7", "7", "7", "7,6"]
        d1 = pandas.DataFrame(dict(name=exp)).reset_index(drop=False)
        d2 = pandas.DataFrame(dict(name=val)).reset_index(drop=False)
        d1.to_csv(st1, index=False, header=None, sep=';')
        d2.to_csv(st2, index=False, header=None, sep=';')
        r = multi_label_jaccard(io.StringIO(st1.getvalue()),
                                io.StringIO(st2.getvalue()))
        self.assertEqual(r, 0.75)


if __name__ == "__main__":
    unittest.main()
