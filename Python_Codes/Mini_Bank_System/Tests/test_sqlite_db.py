def test_create_user(test_db):
    cursor = test_db.cursor
    cursor.execute(
        """
        INSERT INTO users
        (
            username,
            password
        )
        VALUES (?, ?)
        """,
        ("user1", "password123"),
    )
    test_db.conn.commit()
    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        ("user1",),
    )
    user = cursor.fetchone()
    assert user is not None


def test_user_count_empty(test_db):
    cursor = test_db.cursor
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        """)
    count = cursor.fetchone()[0]
    assert count == 0


def test_user_count_one(test_db):
    cursor = test_db.cursor
    cursor.execute(
        """
        INSERT INTO users
        (
            username,
            password
        )
        VALUES (?, ?)
        """,
        ("user1", "password123"),
    )
    test_db.conn.commit()
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        """)
    count = cursor.fetchone()[0]
    assert count == 1


def test_multiple_users(test_db):
    cursor = test_db.cursor
    users = [("user1", "pass1pass"), ("user2", "pass2pass"), ("user3", "pass3pass")]
    cursor.executemany(
        """
        INSERT INTO users
        (
            username,
            password
        )
        VALUES (?, ?)
        """,
        users,
    )
    test_db.conn.commit()
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        """)
    count = cursor.fetchone()[0]
    assert count == 3


def test_find_existing_user(test_db):
    cursor = test_db.cursor
    cursor.execute(
        """
        INSERT INTO users
        (
            username,
            password
        )
        VALUES (?, ?)
        """,
        ("prashant", "password123"),
    )
    test_db.conn.commit()
    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        ("prashant",),
    )
    user = cursor.fetchone()
    assert user is not None


def test_find_non_existing_user(test_db):
    cursor = test_db.cursor
    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        ("ghost",),
    )
    user = cursor.fetchone()
    assert user is None


def test_get_failed_attempts_default(test_db):
    test_db.create_user("prashant", "password123")
    attempts = test_db.get_failed_attempts("prashant")
    assert attempts == 0


def test_update_failed_attempts(test_db):
    test_db.create_user("prashant", "password123")
    test_db.update_failed_attempts("prashant", 2)
    attempts = test_db.get_failed_attempts("prashant")
    assert attempts == 2


def test_update_failed_attempts_multiple_times(test_db):
    test_db.create_user("prashant", "password123")
    test_db.update_failed_attempts("prashant", 1)
    test_db.update_failed_attempts("prashant", 2)
    test_db.update_failed_attempts("prashant", 3)
    attempts = test_db.get_failed_attempts("prashant")
    assert attempts == 3


def test_get_locked_until_default(test_db):
    test_db.create_user("prashant", "password123")
    locked_until = test_db.get_locked_until("prashant")
    assert locked_until is None


def test_lock_user(test_db):
    test_db.create_user("prashant", "password123")
    lock_time = "2099-01-01T00:00:00"
    test_db.lock_user("prashant", lock_time)
    stored_lock_time = test_db.get_locked_until("prashant")
    assert stored_lock_time == lock_time


def test_reset_login_attempts(test_db):
    test_db.create_user("prashant", "password123")
    test_db.update_failed_attempts("prashant", 3)
    test_db.lock_user("prashant", "2099-01-01T00:00:00")
    test_db.reset_login_attempts("prashant")
    attempts = test_db.get_failed_attempts("prashant")
    locked_until = test_db.get_locked_until("prashant")
    assert attempts == 0
    assert locked_until is None


def test_get_user_password_hash(test_db):
    test_db.create_user("prashant", "hashed_password_123")
    stored_hash = test_db.get_user_password_hash("prashant")
    assert stored_hash == "hashed_password_123"
