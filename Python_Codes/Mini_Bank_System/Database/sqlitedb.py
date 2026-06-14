import sqlite3


class SQLiteDB:

    def __init__(self):
        self.conn = sqlite3.connect("Database/xyz_bank.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)
        self.conn.commit()

    def user_exists(self, username):
        self.cursor.execute(
            """
            SELECT username
            FROM users
            WHERE username = ?
            """,
            (username,),
        )
        return self.cursor.fetchone() is not None

    def create_user(self, username, password):
        self.cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password
            )
            VALUES (?, ?)
            """,
            (username, password),
        )
        self.conn.commit()
        return True

    def authenticate_user(self, username, password):

        self.cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username = ?
            AND password = ?
            """,
            (username, password),
        )

        user = self.cursor.fetchone()

        return user is not None


sqlitedb = SQLiteDB()
