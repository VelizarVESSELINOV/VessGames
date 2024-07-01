from datetime import UTC, datetime

from colorlog import debug

from sql.db_connect import db_connect


CURR = db_connect()


def add_user_if_not_exists(session):
    """
    A function to add a user to the database if the user does not already exist.
    It checks if the user exists based on the user_id and user_source provided in the session.
    If the user does not exist, it creates a new user with the information from the session.
    """
    # check if user exists
    CURR.execute(
        "SELECT * FROM vstore.user WHERE user_id = %s AND user_source = %s",
        (session["user_id"], session["user_source"]),
    )

    if not CURR.fetchone():
        # create user
        debug("Creating user")
        CURR.execute(
            """INSERT INTO vstore.user (user_id, user_source,
                nick_name, first_name, last_name, image, location)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (
                session["user_id"],
                session["user_source"],
                session["user_nick_name"],
                session["user_first_name"],
                session["user_last_name"],
                session["user_image"],
                session["user_location"],
            ),
        )


def start_session(user_id, user_source):
    """
    Args:
        user_id (str): The ID of the user.
        user_source (str): The source of the user (e.g., Google).

    Returns:
        datetime: The start time of the session.

    This function checks if the session exists based on the user_id and user_source provided.
    If the session does not exist, it creates a new session with the provided information.
    """

    # Get the current time
    start = datetime.now(UTC).isoformat()

    sql = f"""INSERT INTO vstore.session (user_id, user_source, login)
VALUES ('{user_id}', '{user_source}', '{start}')"""

    debug(f"Start session SQL: {sql}")

    # Create session in the database
    CURR.execute(sql)

    # Return the start time of the session
    return start


def end_session(user_id, user_source, login):
    """
    Args:
        user_id (str): The ID of the user.
        user_source (str): The source of the user (e.g., Google).
        login (datetime): The start time of the session.

    Returns:
        datetime: The end time of the session.

    This function checks if the session exists based on the user_id and user_source provided.
    If the session does not exist, it creates a new session with the provided information.
    """

    # Get the current time
    logout = datetime.now(UTC).isoformat()

    sql = f"""UPDATE vstore.session
SET logout = '{logout}'
WHERE user_id = '{user_id}'
  AND user_source = '{user_source}'
  AND login = '{login}';"""

    debug(f"End session SQL: {sql}")

    # Create session in the database
    ret = CURR.execute(sql)
    ret2 = CURR.rowcount

    debug(ret)
    debug(ret2)

    # Return the end time of the session
