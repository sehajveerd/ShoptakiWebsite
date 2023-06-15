from flask import Flask
from db import db


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Welcome to Real-Estate-AI!'

    db.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
