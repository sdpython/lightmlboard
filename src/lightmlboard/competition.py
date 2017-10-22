# -*- coding: utf-8 -*-
"""
@file
@brief Defines a competition.
"""
from .metrics import mse, sklearn_metric


class Competition:
    """
    Defines a competition.
    """

    def __init__(self, link, name, description, metrics, expected_values=None):
        """
        @param      link                link to the page, something like ``/competition``
        @param      name                name of the competition
        @param      metrics             list of metrics to compute
        @param      description         description
        @param      expected_values     expected values for each metric
        """
        self.link = link
        self.name = name
        self.metrics = metrics if isinstance(metrics, list) else [metrics]
        self.description = description
        self.expected_values = self._load_values(expected_values)

    def _load_values(self, values):
        """
        Converts values into a list of list of values,
        one per metrics.
        """
        if isinstance(values, str):
            import pandas
            df = pandas.read_csv(values, header=None)
            res = [df[df.columns[i]] for i in range(df.shape[1])]
        else:
            res = values if isinstance(values, list) else [values]
        if len(res) != len(self.metrics):
            raise ValueError("Wrong dimensions {0} != {1}.".format(
                len(res), len(self.metrics)))
        return res

    def evaluate(self, values):
        """
        Evaluates received values.

        @param      values      list of values
        @return                 dictionary {metric: res}
        """
        res = {}
        values = self._load_values(values)
        for met, exp, val in zip(self.metrics, self.expected_values, values):
            res[met] = self.evalute_metric(met, exp, val)
        return res

    def evalute_metric(self, met, exp, val):
        """
        Evaluates a metric.

        @param      met     metric
        @param      exp     expected value
        @param      val     values
        @return             result
        """
        if met == "mse":
            return mse(exp, val)
        else:
            return sklearn_metric(met, exp, val)
