from flask import Flask
from .extensions import mail, login_manger, db, cors, mongo
from config import config
from celery import Celery


celery_app = Celery(__name__)
#celery = Celery(__name__)
celery_app.conf.broker_read_url = 'redis://localhost:6379/'#'pyamqp://Akachi:12345Akachi@localhost:5672/flask_host'
celery_app.conf.broker_write_url = "redis://localhost:6379/0"
#celery_app.conf.result_backend = "pyamqp://Akachi:12345Akachi@localhost:5672/flask_host"

def create_app(config_name):

    app = Flask(__name__)
    

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSlify
        sslify = SSlify(app)

    celery_app.conf.update(app.config)
    
    
#EXTENSIONS INITIALIZATION
    login_manger.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    mongo.init_app(app, )

    
    #client.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .stripay import stripay as stripay_blueprint
    app.register_blueprint(stripay_blueprint, url_prefix='/stripy')

    from .paypal import paypal as paypal_blueprint
    app.register_blueprint(paypal_blueprint, url_prefix='/paypal')

    from .data import data as data_blueprint
    app.register_blueprint(data_blueprint, url_prefix='/data')

    return app
