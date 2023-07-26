from flask.cli import AppGroup
from .states import seed_states, delete_states
from .properties import seed_properties, delete_properties

# create a group of commands with the prefix seed
seed_commands = AppGroup("seed")


@seed_commands.command("add_properties")
def add_properties():
    seed_properties()


@seed_commands.command("undo_properties")
def undo_properties():
    delete_properties()


@seed_commands.command("add_states")
def add_states():
    seed_states()


@seed_commands.command("undo_states")
def undo_states():
    delete_states()
