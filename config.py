from lms.canvas import CanvasApi


class Config:
    env = 'DEV'
    db_file = 'app.db'
    api_url = 'https://stedwards.instructure.com/'
    lms = CanvasApi
