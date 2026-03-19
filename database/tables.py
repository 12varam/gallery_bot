from database.connection import connect_to_db


def create_gallery_table():
    connection, cursor = connect_to_db()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS galleries (
        id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        name VARCHAR(255) NOT NULL
    )
    """
    )
    connection.commit()
    connection.close()


def create_images_table():
    connection, cursor = connect_to_db()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        url VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        gallery_id INTEGER REFERENCES galleries(id)
    )
    """
    )
    connection.commit()
    connection.close()
