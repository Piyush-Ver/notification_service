import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI',
        'mysql+pymysql://root:password@localhost/notification_service_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
