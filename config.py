from stats.beta import BetaDistribution


class Config:
    env = 'DEV'
    db_file = 'app.db'
    lms = None


class StEdwardsConfig(Config):
    api_url = 'https://stedwards.instructure.com/'
    distribution = BetaDistribution

    # Done to avoid circular import
    @classmethod
    def load_lms(cls, api_url, api_token):
        if cls.lms is None:
            from lms.canvas import CanvasApi
            cls.lms = CanvasApi(api_url, api_token)
        return cls.lms
