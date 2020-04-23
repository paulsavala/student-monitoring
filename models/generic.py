from config import StEdwardsConfig


class GenericModel:
    def __init__(self):
        self.lms = StEdwardsConfig.load_lms()
