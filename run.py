from app import create_app, db
from flask_script import Manager, Server
from app.models import User, Role
from flask_migrate import Migrate, MigrateCommand

# Create app instance
app = create_app('development')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('server',Server)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()