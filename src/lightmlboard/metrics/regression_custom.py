"""
@file
@brief Metrics about regressions.
"""
import numpy


def l1_reg_max(exp, val, max_val=180):
    """
    Implements a :epkg:`L1` scoring function which does not consider
    error above threshold *max_val*.

    @param      exp     list of values or :epkg:`numpy:array`
    @param      val     list of values or :epkg:`numpy:array`
    @return             score

    .. math::

        E = \frac{1}{n} \sum_{i=1}{n}  \frac{\min \left| Y_i - \min f(X_i) \right|}{180}

    The computation is faster is :epkg:`numpy:array` are used
    (for *exp* and *val*).
    """
    if isinstance(exp, numpy.ndarray) and isinstance(val, numpy.ndarray):
        an = numpy.zeros((len(exp),))
        an[:] = max_val
        mv = numpy.minimum(an, val)
        me = numpy.minimum(an, exp)
        df = numpy.abs(mv - me) / max_val
        return df.mean()
    else:
        r = 0.0
        for e, v in zip(exp, val):
            mv = min(v, max_val)
            ev = min(e, max_val)
            d = abs(mv - ev)
            r += 1. * d / max_val
        return r / len(exp)
