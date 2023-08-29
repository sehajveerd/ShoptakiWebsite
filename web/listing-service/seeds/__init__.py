from flask.cli import AppGroup
from models import db
from .states import seed_states, delete_states
from .properties import seed_properties, delete_properties
from .propertyImages import seed_images, delete_images
from .projects import seed_projects, delete_projects

# create a group of commands with the prefix seed
seed_commands = AppGroup("seed")


@seed_commands.command("create_tables")
def create_tables():
    db.create_all()


@seed_commands.command("add_all")
def add_all():
    seed_states()
    seed_properties()
    seed_images()
    seed_projects()


@seed_commands.command("undo_all")
def undo_all():
    delete_properties()
    delete_states()
    delete_images()
    delete_projects()


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


@seed_commands.command("add_images")
def add_images():
    seed_images()


@seed_commands.command("undo_images")
def undo_images():
    delete_images()


@seed_commands.command("add_projects")
def add_projects():
    seed_projects()


@seed_commands.command("undo_projects")
def undo_projects():
    delete_projects()
