#!/usr/bin/python
from app.app import create_app, register_extensions
from app.config.config import DevelopmentConfig

app = create_app(DevelopmentConfig)
register_extensions(app)

if __name__ == '__main__':
    PORT = int(app.config['PORT'])
    app.run(port=PORT)
