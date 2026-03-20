from database.connection import connect_to_db


def create_tables():
    connection, cursor = connect_to_db()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            tg_chat_id BIGINT UNIQUE,
            tg_username TEXT UNIQUE 
        )
    """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS galleries (
        id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        name VARCHAR(255) NOT NULL,
        user_id INTEGER REFERENCES users(id)
    )
    """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        file_id TEXT NOT NULL,
        description TEXT NOT NULL,
        gallery_id INTEGER REFERENCES galleries(id)
    )
    """
    )
    connection.commit()
    connection.close()
