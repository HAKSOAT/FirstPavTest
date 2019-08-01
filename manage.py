from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.app import create_app, register_extensions
from app.utils.extensions import db
from app.config.config import DevelopmentConfig

app = create_app(DevelopmentConfig)
register_extensions(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
