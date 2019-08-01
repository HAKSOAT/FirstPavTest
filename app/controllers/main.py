from flask import jsonify
from flask_api import status


def error_pages(error):
    error_message_map = {
        status.HTTP_404_NOT_FOUND: "Page doesn't exist",
    }
    return jsonify(message=error_message_map[error.code]), error.code
