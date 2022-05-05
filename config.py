import os
#os.environ.setdefault('FORKED_BY_MULTIPROCESSING','1')
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = 'Unbiased Opinion'
    MAIL_SENDER = os.environ.get('MAIL_SENDER','anabantiakachi1@gmail.com')
    SERVER_ADMIN = os.environ.get('SERVER_ADMIN')
    MONGO_URI = os.environ.get("MONGO_URI")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_NAME='127.0.0.1:5000'
    TWITTER_SECRET = os.environ.get("TWITTER_SECRET")
    TWITTER_KEY = os.environ.get("TWITTER_KEY")
    CORS_HEADERS = 'Content-Type'
    CELERY_BROKER_URL = 'amqp://guest:guest@localhost:6379/'#"redis://localhost:6379" #'pyamqp://Akachi:12345Akachi@localhost:5672/flask_host'
    result_backend= 'redis://redis:6379' #'rpc://'


    @staticmethod
    def init_app(app):
        pass


class DevelopementSetting(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    MONGODB_SETTING ={
        'db':'local',
        'host':'localhost',
        'port':27017
    }
    MONGO_URI='mongodb://localhost:27017'
        
   


class TestingSetting(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

class ProductionSetting(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config ={
    'development':DevelopementSetting,
    'testing':TestingSetting,
    'production':ProductionSetting,
    
    'default':DevelopementSetting
}