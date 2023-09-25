from flask import Flask
from flask_graphql import GraphQLView
from flask_migrate import Migrate
from flask_cors import CORS

from models import db
from config import Config
from seeds import seed_commands
from schema import schema
from utils.consumer import pull_transaction


def create_app():
    app = Flask(__name__)

    app.cli.add_command(seed_commands)

    app.config.from_object(Config)
    db.init_app(app)
    Migrate(app, db)

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
    )

    # Configure CORS to allow requests from your frontend origin
    CORS(app, resources={
        r"/graphql": {"origins": "http://localhost:3001"}})

    @app.before_request
    def create_tables():
        db.create_all()

    @app.route("/")
    def index():
        return "Welcome to Real-Estate-AI!"

    # TODO: For testing purposes only. The consumer.py should be run in another thread.
    @app.route("/consume")
    def pull_msg():
        pull_transaction()
        return "Transaction processing started"
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
