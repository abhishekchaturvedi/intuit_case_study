import click

from sqlalchemy_utils import database_exists, create_database

from userlogin.app import create_app
from userlogin.app import db
from userlogin.blueprints.user.models import User

# Create an app context for the database connection.
app = create_app()
db.app = app


@click.group()
def cli():
    """ Run PostgreSQL related tasks. """
    pass


@click.command()
def init():
    """
    Initialize the database.

    :return: None
    """
    db.drop_all()
    db.create_all()

    return None


@click.command()
def seed():
    """
    Seed the database with an initial user.

    :return: User instance
    """
    if User.find_user(app.config['SEED_ADMIN_EMAIL']) is not None:
        return None

    params = {
        'role': 'admin',
        'email': app.config['SEED_ADMIN_EMAIL'],
        'password': app.config['SEED_ADMIN_PASSWORD']
    }

    return User(**params).save()


@click.command()
@click.pass_context
def reset(ctx):
    """
    Init and seed automatically.

    :return: None
    """
    ctx.invoke(init)
    ctx.invoke(seed)

    return None


cli.add_command(init)
cli.add_command(seed)
cli.add_command(reset)
