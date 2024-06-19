import asyncio
from logging.config import fileConfig

from alembic import context

from app.core.configs import AsyncpgDbConfigSchema
from app.core.db.models import Base
from sqlalchemy.ext.asyncio import create_async_engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.


# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

# TODO: надо разобраться как здесь лучше сделать?
def render_item(type_: str, col, autogen_context) -> str | bool:
    if col is None:
        return False

    if (
            type_ == 'type'
            and col.__class__.__module__ == 'gino.schema'
            and col.__class__.__name__ == 'Enum'
    ):
        return f'sa.{col!r}'

    if (
            type_ == 'server_default'
            and col.column.type.__module__ == 'app.core.db.types'
            and col.column.type.__class__.__name__ in ('TxIdSnapshot', 'TxIdCurrent')
    ):
        return str(col.arg)

    return False


def include_object(object, name, type_, reflected, compare_to):
    return not (type_ == 'table' and object.schema == 'cron')


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=include_object,
        include_schemas=True,
        compare_type=True,
        compare_server_default=True,
        render_item=render_item,

        version_table_schema=target_metadata.schema,
    )

    with context.begin_transaction() as tx:
        context.run_migrations()
        if 'dry-run' in context.get_x_argument():
            print('Dry-run succeeded; now rolling back transaction...')
            tx.rollback()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_async_engine(str(AsyncpgDbConfigSchema().DSN), future=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
