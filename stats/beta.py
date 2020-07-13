import math
from scipy.stats import beta


class BetaDistribution:
    def __init__(self, a=None, b=None, default_left=0, default_right=1):
        self.a = a
        self.b = b
        self.default_left = default_left
        self.default_right = default_right

    def pdf(self, x, a, b):
        assert self.a is not None and self.b is not None, 'Params have not been set. First run .fit()'
        x = range(0, 1, 0.01)
        return x, beta.pdf(x, self.a, self.b)
        raise NotImplementedError

    def cdf(self, x, a, b):
        raise NotImplementedError

    def ppf(self, p, a, b):
        raise NotImplementedError

    def fit(self, grades):
        mu = math.mean(grades)
        n = len(grades)
        a = mu * n
        b = (1 - mu) * n
        self.a = a
        self.b = b

    def conf_int(self, conf_level=0.05):
        assert self.a is not None and self.b is not None, 'Params have not been set. First run .fit()'
        # Handles case where uses specifies something like 95% CI
        if conf_level > 0.5:
            conf_level = 1 - conf_level
        left = beta.ppf(conf_level / 2, self.a, self.b)
        right = beta.ppf(1 - conf_level / 2, self.a, self.b)

        # Used because the ppf will never return 1, only 0.9999...
        left = math.round(left, 1)
        right = math.round(right, 1)
        if np.isnan(left):
            left = self.default_left
        if np.isnan(right):
            right = self.default_right

        return left, right

    def p_value(self, x, assignment_collection, one_tailed=False):
        assert self.a is not None and self.b is not None, 'Params have not been set. First run .fit()'
        tail = beta.cdf(x, self.a, self.b)
        tail = min(tail, 1 - tail)
        if one_tailed:
            return tail
        else:
            return 2 * tail
