import os
import sqlite3
import pytest

TEST_DB = "Tests/test_bank.db"


@pytest.fixture
def test_db():

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE users
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    yield conn
    conn.close()

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
