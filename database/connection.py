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


def get_user_id(tg_chat_id):
    connection, cursor = connect_to_db()

    cursor.execute("SELECT id FROM users WHERE tg_chat_id = %s", (tg_chat_id,))
    user_id = cursor.fetchone()
    connection.commit()
    connection.close()
    if user_id:
        return user_id[0]
    else:
        return None


def add_new_gallery(tg_chat_id, gallery_name):
    connection, cursor = connect_to_db()

    cursor.execute(
        "SELECT id FROM users WHERE tg_chat_id = (%s)",
        (tg_chat_id,),
    )
    user_id = cursor.fetchone()
    
    if user_id:
        user_id = user_id[0]
        
        cursor.execute(
            "INSERT INTO galleries (name, user_id) VALUES (%s, %s)",
            (gallery_name, user_id)
        )
    
    connection.commit()
    connection.close()
