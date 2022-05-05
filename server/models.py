import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from .extensions import db, login_manger
from werkzeug.security import generate_password_hash, check_password_hash

class StripeCustomer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    StripeCustomerId = db.Column(db.String(255), nullable=False)
    StripeSubscriptionId = db.Column(db.String(255), nullable = False, unique=True)

        

class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, index=True)
    username = db.Column(db.String(64), unique=False, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    #about_me = db.Column(db.String(255), unique=True)
    #created_on = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    #country = db.Column(db.String(255))
    #postal_code = db.Column(db.Integer)
    #address = db.Column(db.String(255))



    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({ 'confirm':self.id }).decode('utf-8')

    def confirm(self, token):
        s= Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        return True

@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

