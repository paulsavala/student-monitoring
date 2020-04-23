import numpy as np
from scipy.stats import beta


class GenericDistribution:
    def __init__(self, **kwargs):
        pass

    def fit(self, assignment_collection):
        raise NotImplementedError

    def conf_int(self, assignment_collection, conf_level=0.05):
       raise NotImplementedError

    def pdf(self, assignment_collection):
        raise NotImplementedError

    def p_value(self, x, assignment_collection, one_tailed=False):
        raise NotImplementedError
