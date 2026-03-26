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


def register_user(tg_chat_id, tg_username):
    connection, cursor = connect_to_db()

    cursor.execute(
        """
        INSERT INTO users (tg_chat_id, tg_username) 
        VALUES (%s, %s) 
        ON CONFLICT (tg_chat_id) DO NOTHING
    """,
        (tg_chat_id, tg_username),
    )

    connection.commit()
    connection.close()


def get_user_id(cursor, tg_chat_id):
    cursor.execute("SELECT id FROM users WHERE tg_chat_id = %s", (tg_chat_id,))
    user_id = cursor.fetchone()
    return user_id[0] if user_id else None


def get_gallery_id(cursor, gallery_name, tg_chat_id):
    user_id = get_user_id(cursor, tg_chat_id)

    cursor.execute(
        "SELECT id FROM galleries WHERE name = %s AND user_id = %s",
        (gallery_name, user_id),
    )
    result = cursor.fetchone()

    return result[0] if result else None


def add_new_gallery(tg_chat_id, gallery_name):
    connection, cursor = connect_to_db()

    user_id = get_user_id(cursor, tg_chat_id)

    if user_id:
        cursor.execute(
            "INSERT INTO galleries (name, user_id) VALUES (%s, %s)",
            (gallery_name, user_id),
        )

    connection.commit()
    connection.close()


def get_galleries(tg_chat_id):
    connection, cursor = connect_to_db()

    user_id = get_user_id(cursor, tg_chat_id)

    if user_id:
        cursor.execute("SELECT name FROM galleries WHERE user_id = %s", (user_id,))
        gallery_names = cursor.fetchall()
    else:
        gallery_names = []

    connection.close()
    return gallery_names


def delete_gallery(tg_chat_id, gallery_name):
    connection, cursor = connect_to_db()

    user_id = get_user_id(cursor, tg_chat_id)

    if user_id:
        cursor.execute(
            "DELETE FROM galleries WHERE name = %s AND user_id = %s",
            (gallery_name, user_id),
        )

    connection.commit()
    connection.close()


def update_gallery_name(tg_chat_id, old_name, new_name):
    connection, cursor = connect_to_db()

    user_id = get_user_id(cursor, tg_chat_id)

    if user_id:
        cursor.execute(
            """
            UPDATE galleries 
            SET name = %s 
            WHERE name = %s AND user_id = %s
            """,
            (new_name, old_name, user_id),
        )

    connection.commit()
    connection.close()


def get_gallery_images(tg_chat_id, gallery_name):
    connection, cursor = connect_to_db()

    gallery_id = get_gallery_id(cursor, gallery_name, tg_chat_id)

    images = []
    if gallery_id:
        cursor.execute(
            "SELECT file_id, description FROM images WHERE gallery_id = %s",
            (gallery_id,),
        )
        images = cursor.fetchall()

    connection.close()
    return images


def add_image_to_db(tg_chat_id, file_id, gallery_name, description=""):
    connection, cursor = connect_to_db()

    gallery_id = get_gallery_id(cursor, gallery_name, tg_chat_id)

    if gallery_id:
        cursor.execute(
            "INSERT INTO images (file_id, gallery_id, description) VALUES (%s, %s, %s)",
            (file_id, gallery_id, description),
        )
        connection.commit()

    connection.close()


def remove_photo_from_db(tg_chat_id, file_id, gallery_name):
    connection, cursor = connect_to_db()

    gallery_id = get_gallery_id(cursor, gallery_name, tg_chat_id)

    if gallery_id:
        cursor.execute("DELETE FROM images WHERE file_id = %s", (file_id,))
        connection.commit()

    connection.close()
