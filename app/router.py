from .controllers import main, user, quiz
from flask_api import status


def routes(app):
    """Manages all routes.
    This app uses an MVC pattern, hence all the URLs are routed here.
    Import logic from the controllers and route using
    the add_url_rule function

    :param app: Flask app instance
    :return: None
    """

    app.register_error_handler(status.HTTP_404_NOT_FOUND, main.error_pages)

    # Add your Url rules here
    app.add_url_rule('/user/register', 'user.register',
                     view_func=user.register, methods=["POST"])
    app.add_url_rule('/quiz/create', 'quiz.create',
                     view_func=quiz.create, methods=["POST"])
    app.add_url_rule('/quiz/<int:quiz_id>/view',
                     'quiz.view', view_func=quiz.view, methods=["GET"])
    app.add_url_rule('/quiz/<int:quiz_id>/solve',
                     'quiz.solve', view_func=quiz.solve, methods=["POST"])
