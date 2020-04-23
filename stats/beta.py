import numpy as np
from scipy.stats import beta


class BetaDistribution:
    def __init__(self, a=None, b=None):
        self.a = self.a
        self.b = self.b

    def fit(self, grades):
        mu = np.mean(grades)
        n = len(grades)
        a = mu * n
        b = (1 - mu) * n
        self.a = a
        self.b = b

    def conf_int(self, grades, conf_level=0.05):
        assert self.a is not None and self.b is not None, 'Params have not been set. First run .fit()'
        if conf_level > 0.5:
            conf_level = 1 - conf_level
        left = beta.ppf(conf_level / 2, self.a, self.b)
        right = beta.ppf(1 - conf_level / 2, self.a, self.b)

        left = np.round(left, 2)
        right = np.round(right, 2)
        if np.isnan(left):
            left = 0
        if np.isnan(right):
            right = 1
        return left, right

    def pdf(self, grades):
        assert self.a is not None and self.b is not None, 'Params have not been set. First run .fit()'
        x = np.linspace(0, 1, 101)
        return x, beta.pdf(x, self.a, self.b)

    def p_value(self, x, assignment_collection, one_tailed=False):
        assert self.a is not None and self.b is not None, 'Params have not been set. First run .fit()'
        tail = beta.cdf(x, self.a, self.b)
        tail = min(tail, 1 - tail)
        if one_tailed:
            return tail
        else:
            return 2 * tail
