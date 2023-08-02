from flask import Flask
from flask_graphql import GraphQLView
from flask_migrate import Migrate

from models import db
from config import Config
from seeds import seed_commands
from schema import schema


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

    @app.before_request
    def create_tables():
        db.create_all()

    @app.route("/")
    def index():
        return "Welcome to Real-Estate-AI!"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
