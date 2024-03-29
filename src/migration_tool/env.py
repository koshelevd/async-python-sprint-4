from alembic import context
from sqlalchemy import create_engine, pool

# noqa
import db.tables
from db.utils.db_session import Base


config = context.config

target_metadata = Base.metadata


def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    context.configure(
        url=config.get_main_option('sqlalchemy.url'),
        include_schemas=True,
        version_table_schema=target_metadata.schema,
        target_metadata=[target_metadata, ],
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = create_engine(config.get_main_option('sqlalchemy.url'),
                                poolclass=pool.NullPool)

    def include_name(name, type_, parent_names):
        if type_ == "schema":
            return name in [target_metadata.schema, ]
        else:
            return True

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=[target_metadata, ],
            include_schemas=True,
            version_table_schema=target_metadata.schema,
            include_name=include_name,
        )

        connection.execute(
            f"CREATE SCHEMA IF NOT EXISTS {target_metadata.schema};"
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
