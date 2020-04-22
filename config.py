from lms.canvas import CanvasApi


class Config:
    env = 'DEV'
    db_file = 'app.db'


class StEdwardsConfig(Config):
    lms = CanvasApi
