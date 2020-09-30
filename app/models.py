from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    assessment = db.Column(db.String(20), nullable = False)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))    

    def __repr__(self):
        return f'User ({self.username})'


# Role data-model
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'

# UserRoles association table
# class UserRoles(db.Model):
#     __tablename__ = 'user_roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

 class Grades(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    test_id = db.Column(db.Integer,db.ForeignKey('test.id'))
    

    def save(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_grades(cls,id):
        grades = Grades.query.filter_by(test_id=id).all()
        return grade

    def __repr__(self):
        return f'{self.user_id}:{self.test_id}'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)  