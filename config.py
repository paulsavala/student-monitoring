from stats.beta import BetaDistribution
from lms.lms import Canvas

import os


basedir = os.path.abspath(os.path.dirname(__file__))


class GenericConfig:
    ENV = 'DEV'
    DB_ENDPOINT = os.environ.get('DATABASE_URL') or 'sqlite://' + os.path.join(basedir, 'app.db')
    COURSE_SUMMARY_STAT = 'median'  # or 'mean'
    COMMIT_OUTLIERS_TO_DB = False
    TESTING = False


class StEdwardsConfig(GenericConfig):
    # id in schools table in db
    SCHOOL_ID = 1
    # Canvas API endoint
    LMS_URL = 'https://stedwards.instructure.com/'
    # Lambda API abstraction layer endpoint
    API_BASE_URL = 'https://student-monitoring-lms-api.herokuapp.com/v1.0'
    # Used to make CI
    DISTRIBUTION = BetaDistribution
    # How datetimes are stored
    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
    # COMMIT_OUTLIERS_TO_DB = True
    # Used for getting current courses from LMS
    SEMESTER = 'Fall 2020'
    # Email address to show in "from" field
    FROM_EMAIL = 'weeklyupdate@lululearner.com'
    # LMS system
    LMS = Canvas


class StEdwardsTestConfig(StEdwardsConfig):
    TESTING = True