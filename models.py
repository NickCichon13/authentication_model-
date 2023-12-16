from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)

db = SQLAlchemy()

def connect_db(app):

    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.Text,primary_key = True, unique = True, nullable = False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable = False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, username,email, pwd, first_name, last_name):
# Register user with hashed password & return user
        hashed = bcrypt.generate_password_hash(pwd)
#  turn bytestring into normal (unicode utf8) code
        hashed_utf8 = hashed.decode("utf8")
#  return instance of user with username and hashed pwd
        return cls(username=username, email=email, password=hashed_utf8, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
# Validate that the user exists and the password is correct.
# If the user is valid return username, else return Fasle.

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

    
class Feedback(db.Model):
    
        __tablename__ = 'feedbacks'

        id = db.Column(db.Integer, primary_key = True, autoincrement=True, unique = True )
    
        title = db.Column(db.Text, nullable = False)
    
        content = db.Column(db.Text, nullable = False)
    
    # username_id = db.Column(db.Integer, db.ForeignKey('username'), nullable=False)
