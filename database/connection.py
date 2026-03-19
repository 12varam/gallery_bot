from psycopg2 import connect
from config.loader import settings


def connect_to_db():
    connection = connect(
        host=settings.db.host,
        database=settings.db.name,
        user=settings.db.user,
        password=settings.db.password,
        port=settings.db.port,
    )
    cursor = connection.cursor()

    return connection, cursor
