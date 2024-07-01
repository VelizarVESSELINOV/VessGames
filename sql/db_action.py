from datetime import UTC, datetime

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
    start = datetime.now(UTC)

    # Create session in the database
    CURR.execute(
        # SQL query to insert a new session
        "INSERT INTO vstore.session (user_id, user_source, login) VALUES (%s, %s, %s)",
        # Values to insert into the session table
        (user_id, user_source, start),
    )

    # Return the start time of the session
    return start


def end_session(user_id, user_source, start):
    """
    Args:
        user_id (str): The ID of the user.
        user_source (str): The source of the user (e.g., Google).
        start (datetime): The start time of the session.

    Returns:
        datetime: The end time of the session.

    This function checks if the session exists based on the user_id and user_source provided.
    If the session does not exist, it creates a new session with the provided information.
    """

    # Get the current time
    end = datetime.now(UTC)

    # Create session in the database
    CURR.execute(
        # SQL query to insert a new session
        "UPDATE vstore.session SET end = %s WHERE user_id = %s AND user_source = %s AND login = %s",
        # Values to insert into the session table
        (end, user_id, user_source, start),
    )

    # Return the end time of the session
