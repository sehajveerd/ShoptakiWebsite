import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
from models import userDetail
from models import db
from seeds import seed_commands


def setup_auth0(app):
    # Define the Auth0 routes and configuration
    oauth = OAuth(app)

    oauth.register(
        "auth0",
        client_id=env.get("AUTH0_CLIENT_ID"),
        client_secret=env.get("AUTH0_CLIENT_SECRET"),
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
    )

    @app.route("/callback", methods=["GET", "POST"])
    def callback():
        token = oauth.auth0.authorize_access_token()

        userinfo_response = oauth.auth0.get(
            "https://dev-0at54ebe72reuvqj.us.auth0.com/userinfo"
        )
        userinfo = userinfo_response.json()

        # Extract the relevant user information
        auth0Id = userinfo.get("sub")
        emailId = userinfo.get("name")
        # ... additional user information you want to store
        role = "buyer"

        # Check if the user already exists
        existing_user = userDetail.query.filter_by(auth0Id=auth0Id).first()

        if existing_user:
            # User already exists, perform the necessary actions
            # You may update the existing user's information or perform any other logic

            # Store the user information in the session
            session["user"] = token
            return redirect("/")
        else:
            # Store the user information in flask session.
            new_user = userDetail(emailId=emailId, auth0Id=auth0Id, role=role)
            db.session.add(new_user)
            db.session.commit()

            session["user"] = token
            return redirect("/")

    @app.route("/login")
    def login():
        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for("callback", _external=True)
        )

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(
            "https://"
            + env.get("AUTH0_DOMAIN")
            + "/v2/logout?"
            + urlencode(
                {
                    "returnTo": url_for("home", _external=True),
                    "client_id": env.get("AUTH0_CLIENT_ID"),
                },
                quote_via=quote_plus,
            )
        )


def setup_graphql(app):
    # Import your schema and GraphQLView
    from schema.user_schema import schema
    from flask_graphql import GraphQLView

    # Define the GraphQL endpoint
    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
    )


def create_app():
    app = Flask(__name__)
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

    # Manually defined in .env
    app.secret_key = env.get("APP_SECRET_KEY")

    app.config["SQLALCHEMY_DATABASE_URI"] = env.get("SQLALCHEMY_DATABASE_URI").replace(
        "postgres://", "postgresql://"
    )

    app.cli.add_command(seed_commands)

    db.init_app(app)

    # setup_auth0(app)  # Call the function to set up Auth0
    setup_graphql(app)  # Call the function to set up the GraphQL endpoint

    @app.route("/")
    def home():
        return render_template(
            "index.html",
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
