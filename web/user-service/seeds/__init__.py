from flask.cli import AppGroup
from models import db
from .users import seed_users, delete_users

# create a group of commands with the prefix seed
seed_commands = AppGroup("seed")


@seed_commands.command("create_tables")
def create_tables():
    db.create_all()


@seed_commands.command("add_users")
def add_users():
    seed_users()


@seed_commands.command("undo_users")
def undo_users():
    delete_users()
