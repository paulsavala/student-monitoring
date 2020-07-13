from stats.beta import BetaDistribution
import datetime


class Config:
    ENV = 'DEV'
    DB_ENDPOINT = None
    DB_USERNAME = None
    LMS = None
    COURSE_SUMMARY_STAT = 'median'  # or 'mean'
    COMMIT_OUTLIERS_TO_DB = False


class StEdwardsConfig(Config):
    # id in schools table in db
    SCHOOL_ID = 1
    # Canvas API endoint
    LMS_URL = 'https://stedwards.instructure.com/'
    # Lambda API abstraction layer endpoint
    API_BASE_URL = 'https://ve9e8bak70.execute-api.us-east-1.amazonaws.com/default'
    # Used to make CI
    DISTRIBUTION = BetaDistribution
    # How datetimes are stored
    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
    # COMMIT_OUTLIERS_TO_DB = True
    # Used for getting current courses from LMS
    SEMESTER = 'Spring 2020'
    # LMS name, needed when invoking the Lambda function lms_api
    LMS = 'Canvas'

    # DB credentials
    DB_ENDPOINT = 'student-monitoring-prod-db.cdchqhkfi2bg.us-east-1.rds.amazonaws.com'
    DB_USERNAME = 'admin_prod'

    # Used for testing
    semester_first_sunday = datetime.datetime(2020, 1, 19)
    semester_last_sunday = datetime.datetime(2020, 5, 3)
    REF_DATE = semester_last_sunday - datetime.timedelta(weeks=4)
