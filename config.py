

class Config:
    env = 'DEV'
    db_file = 'app.db'


class StEdwardsConfig(Config):
    api_url = 'https://stedwards.instructure.com/'

    # Done to avoid circular import
    @staticmethod
    def load_lms(api_url, api_token):
        from lms.canvas import CanvasApi
        return CanvasApi(api_url, api_token)
