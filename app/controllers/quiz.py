from app.models import models
from app.utils.extensions import auth, db
from flask import abort, g, jsonify, request
import math
import pandas as pd


def create():
    try:
        csv = request.files["data"].stream
    except KeyError as e:
        return jsonify(message="{} not found".format(e)), 400
    quiz = models.Quiz()
    db.session.add(quiz)
    db.session.commit()
    current_quiz = models.Quiz.query.order_by(models.Quiz.id.desc()).first()
    current_quiz_id = current_quiz.id
    last_qa = models.QA.query.order_by(models.QA.id.desc()).first()
    current_qa_id = (last_qa.id + 1) if last_qa else 1
    df = pd.read_csv(csv)
    for _, row in df.iterrows():
        try:
            qa = models.QA(question=row["Question"], answer=row["Answer"], quiz_id=current_quiz_id)
            options = models.Options(a=row["Option A"], b=row["Option B"], c=row["Option C"],
                                     d=row["Option D"], quiz_id=current_quiz_id, qa_id=current_qa_id)
        except KeyError as e:
            return jsonify(message="{} column missing".format(e)), 400
        db.session.add(qa)
        db.session.add(options)
        current_qa_id += 1
    db.session.commit()
    return jsonify(message="Quiz created successfully")


def view(quiz_id):
    QAs = models.QA.query.filter_by(quiz_id=quiz_id).all()
    if QAs:
        questions = [qa.question for qa in QAs]
        answers = [qa.answer for qa in QAs]
        options = models.Options.query.filter_by(quiz_id=quiz_id).all()
        options_a = [option.a for option in options]
        options_b = [option.b for option in options]
        options_c = [option.c for option in options]
        options_d = [option.d for option in options]
        return jsonify(
            questions=questions,
            answers=answers,
            options_a=options_a,
            options_b=options_b,
            options_c=options_c,
            options_d=options_d
        )
    else:
        abort(404)


@auth.login_required
def solve(quiz_id):
    QAs = models.QA.query.filter_by(quiz_id=quiz_id).all()
    if QAs:
        json = request.get_json()
        try:
            user_answers = json["answers"]
        except KeyError as e:
            return jsonify(message="{} not found".format(e)), 400
        answers = [qa.answer for qa in QAs]
        if len(answers) != len(user_answers):
            return jsonify(message="{} answers are not available".format(len(answers))), 400
        score = 0
        for answer, user_answer in zip(answers, user_answers):
            if answer == user_answer:
                score += 1
        percentage = math.ceil(score/len(answers) * 100)
        user_id = g.user.id
        user_score = models.Score.query.filter_by(quiz_id=quiz_id).\
            filter_by(user_id=user_id).first()
        if user_score:
            user_score.score = percentage
        else:
            user_score = models.Score(score=percentage, quiz_id=quiz_id, user_id=user_id)
        db.session.add(user_score)
        db.session.commit()
        return jsonify(message="Score is {} percent".format(percentage))
    else:
        abort(404)