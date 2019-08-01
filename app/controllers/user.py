from app.models import models
from app.utils.extensions import bcrypt, auth, db
from flask import jsonify, g, request
import sqlalchemy as sa


def register():
    try:
        json = request.get_json()
        username = json["username"]
        password = json["password"]
    except KeyError as e:
        return jsonify(message="{} not found".format(e)), 400
    password_hash = bcrypt.generate_password_hash(password).decode('utf8')
    user = models.User(username=username, password_hash=password_hash)
    try:
        db.session.add(user)
        db.session.commit()
    except sa.exc.IntegrityError:
        return jsonify(message="Account already exists"), 400
    return jsonify(message="Account created successfully")


@auth.verify_password
def verify_password(username, password):
    user = models.User.query.filter_by(username=username).first()
    if user:
        if bcrypt.check_password_hash(user.password_hash, password):
            g.user = user
            return True
    return False
