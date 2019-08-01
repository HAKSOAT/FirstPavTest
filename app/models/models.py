from app.utils.extensions import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String(128))
    scores = db.relationship('Score', backref='user', lazy=False)

    def __repr__(self):
        return 'Id: {}, name: {}'.format(self.id, self.username)


class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    qas = db.relationship('QA', backref='quiz', lazy=False)
    scores = db.relationship('Score', backref='quiz', lazy=False)
    options = db.relationship('Options', backref='quiz', lazy=False)


class Score(db.Model):
    __tablename__ = "score"
    __table_args__ = (db.UniqueConstraint('quiz_id', 'user_id'),)
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class QA(db.Model):
    __tablename__ = 'qa'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    options = db.relationship('Options', backref='qa', lazy=False)


class Options(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.String)
    b = db.Column(db.String)
    c = db.Column(db.String)
    d = db.Column(db.String)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    qa_id = db.Column(db.Integer, db.ForeignKey('qa.id'), nullable=False)




