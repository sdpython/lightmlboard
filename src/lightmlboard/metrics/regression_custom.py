"""
@file
@brief Metrics about regressions.
"""
import numpy


def l1_reg_max(exp, val, max_val=180):
    """
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
