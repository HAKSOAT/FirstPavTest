from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
auth = HTTPBasicAuth()
db = SQLAlchemy()
