import os
import pytest

from Database.sqlitedb import SQLiteDB

TEST_DB = "Tests/test_bank.db"


@pytest.fixture
def test_db():

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    db = SQLiteDB(TEST_DB)

    yield db

    db.conn.close()

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)