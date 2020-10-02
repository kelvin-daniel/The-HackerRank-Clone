from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,current_user
from . import login_manager
import unicodedata


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def getStandings():
	users = User.query.order_by(User.score.desc())
	return users

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String(1000),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    score = db.Column(db.Integer, nullable=False)
    answered = db.Column(db.PickleType)

    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')


    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):

        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'User {self.username}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'

class Questions(db.Model):
	__tablename__ = 'quizquestions1'

	question = db.Column(db.String, nullable=False)
	option1 = db.Column(db.String, nullable=False)
	option2 = db.Column(db.String, nullable=False)
	option3 = db.Column(db.String, nullable=False)
	option4 = db.Column(db.String, nullable=False)
	answer = db.Column(db.String, nullable=False)
	creatorid = db.Column(db.String, nullable=False)
	questionid = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String, nullable=False)
	difficulty = db.Column(db.String, nullable=False)

	def __repr__(self):
		return "<Question id is %s and creatorid is %s" % (self.questionid, self.creatorid)