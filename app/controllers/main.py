from flask import jsonify


def error_pages(error):
    error_message_map = {
        404: "Page doesn't exist",
    }
    return jsonify(message=error_message_map[error.code]), error.code
