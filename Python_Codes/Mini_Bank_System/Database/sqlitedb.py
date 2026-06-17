import sqlite3
from Backend.security import verify_password


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
                username TEXT UNIQUE Not Null,
                password TEXT Not Null,
                failed_attempts INTEGER DEFAULT 0,
                locked_until TEXT
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
        stored_hash = sqlitedb.get_user_password_hash(username)
        if stored_hash is None:
            return (False, "Invalid Username or Password")
        if not verify_password(password, stored_hash):
            return (False, "Invalid Username or Password")
        return (True, "Login Successful")

    def get_user_password_hash(self, username):

        self.cursor.execute(
            """
            SELECT password
            FROM users
            WHERE username = ?
            """,
            (username,),
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def get_failed_attempts(self, username):
        self.cursor.execute(
            """
            SELECT failed_attempts
            FROM users
            WHERE username = ?
            """,
            (username,),
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return 0

    def get_locked_until(self, username):
        self.cursor.execute(
            """
            SELECT locked_until
            FROM users
            WHERE username = ?
            """,
            (username,),
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def update_failed_attempts(self, username, attempts):
        self.cursor.execute(
            """
            UPDATE users
            SET failed_attempts = ?
            WHERE username = ?
            """,
            (attempts, username),
        )
        self.conn.commit()

    def lock_user(self, username, lock_until):
        self.cursor.execute(
            """
            UPDATE users
            SET locked_until = ?
            WHERE username = ?
            """,
            (lock_until, username),
        )
        self.conn.commit()

    def reset_login_attempts(self, username):
        self.cursor.execute(
            """
            UPDATE users
            SET failed_attempts = 0,
                locked_until = NULL
            WHERE username = ?
            """,
            (username,),
        )
        self.conn.commit()


sqlitedb = SQLiteDB()
