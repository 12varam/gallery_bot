from database.connection import connect_to_db, get_user_id


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
        description TEXT,
        gallery_id INTEGER REFERENCES galleries(id) ON DELETE CASCADE
    )
    """
    )
    connection.commit()
    connection.close()


def delete_tables():
    connection, cursor = connect_to_db()

    cursor.execute(
        """
        DROP TABLE IF EXISTS images CASCADE;
        DROP TABLE IF EXISTS galleries CASCADE;
        DROP TABLE IF EXISTS users CASCADE;
    """
    )

    connection.commit()
    connection.close()
    print("All tables have been deleted successfully")


def check_gallery_exists(tg_chat_id, gallery_name):
    connection, cursor = connect_to_db()
    user_id = get_user_id(cursor, tg_chat_id)

    cursor.execute(
        "SELECT 1 FROM galleries WHERE name = %s AND user_id = %s",
        (gallery_name, user_id),
    )
    exists = cursor.fetchone() is not None
    connection.close()
    return exists
