from flask.cli import AppGroup
from models import db

# create a group of commands with the prefix seed
seed_commands = AppGroup("seed")


@seed_commands.command("create_tables")
def create_tables():
    db.create_all()
