"""
@file
@brief Implements metrics.
"""
import sklearn.metrics as metrics
from .regression import mse


def sklearn_metric(met, exp, val):
    """
    Looks into metrics available in
    :epkg:`scikit-learn:metrics`.

    @param      met     function name
    @param      exp     expected values
    @param      val     values
    @return             number
    """
    if hasattr(metrics, met):
        f = getattr(metrics, met)
        return f(exp, val)
    else:
        raise AttributeError("Unable to find metric '{0}'.".format(met))
