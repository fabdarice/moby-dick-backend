import logging
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database

from app.models.base import BaseModel
from app.models.hodler import HodlerModel  # noqa
from app.models.token import TokenModel  # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = BaseModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# here we allow ourselves to pass interpolation vars to alembic.ini
# fron the host env


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    db_uri = os.environ.get('DATABASE_URL')
    try:
        create_database(db_uri)
    except Exception:
        logging.info('Failed to create database.  Probably already exists.')

    connectable = create_engine(db_uri)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
