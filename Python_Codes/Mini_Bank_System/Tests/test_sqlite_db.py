def test_create_user(test_db):
    cursor = test_db.cursor()
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

    test_db.commit()

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
    cursor = test_db.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        """)

    count = cursor.fetchone()[0]
    assert count == 0


def test_user_count_one(test_db):
    cursor = test_db.cursor()
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

    test_db.commit()
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        """)

    count = cursor.fetchone()[0]
    assert count == 1


def test_multiple_users(test_db):
    cursor = test_db.cursor()
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

    test_db.commit()
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        """)

    count = cursor.fetchone()[0]
    assert count == 3


def test_find_existing_user(test_db):
    cursor = test_db.cursor()
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

    test_db.commit()
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
    cursor = test_db.cursor()
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
