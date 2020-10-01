from app import db
from .models import User

db.create_all()
db.session.add(User('admin', 'admin', 'admin', 0))
db.session.commit()