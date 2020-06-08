from stats.beta import BetaDistribution


class Config:
    env = 'DEV'
    db_file = 'app.db'
    lms = None
    course_summary_stat = 'median'  # or 'mean'
    commit_outliers_to_db = False


class StEdwardsConfig(Config):
    api_url = 'https://stedwards.instructure.com/'
    distribution = BetaDistribution
    datetime_format = '%Y-%m-%dT%H:%M:%SZ'
    # commit_outliers_to_db = True
    semester = 'Spring 2020'

    # Done to avoid circular import
    @classmethod
    def load_lms(cls, api_url, api_token):
        if cls.lms is None:
            from lms.canvas import CanvasApi
            cls.lms = CanvasApi(api_url, api_token)
        return cls.lms
