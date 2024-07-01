from datetime import UTC, datetime
from requests import get
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


def transform_dict_to_postgresql_format(data):
    # Split the 'loc' field into 'latitude' and 'longitude'
    latitude, longitude = map(float, data["loc"].split(","))

    # Create the transformed dictionary
    geo_data = {
        "latitude": latitude,
        "longitude": longitude,
        "postal": data.get("postal"),
        "city": data.get("city"),
        "ip": data.get("ip"),
        "hostname": data.get("hostname"),
        "ip_org": data.get("org"),
        "timezone": data.get("timezone"),
        "country_iso2_code": data.get("country"),
        "region_iso_code": data.get("region"),
    }

    return geo_data


def get_location(user_ip):
    if user_ip is None or user_ip == "127.0.0.1":
        return {
            "latitude": None,
            "longitude": None,
            "postal": None,
            "city": None,
            "ip": None,
            "hostname": None,
            "ip_org": None,
            "timezone": None,
            "country_iso2_code": None,
            "region_iso_code": None,
        }

    # Replace 'your_api_key_here' with your actual API key from a geolocation service
    geoloc_url = f"ipinfo.io/{user_ip}?token=eccc7b89be8042"

    # Make a request to the geolocation API
    response = get(geoloc_url)

    # Check if the request was successful
    if response.status_code == 200:
        data = transform_dict_to_postgresql_format(response.json())
        return data


def start_session(user_id, user_source, user_ip):
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
    geo_data = get_location(user_ip)

    sql = """INSERT INTO vstore.session (user_id, user_source,
login, latitude, longitude, postal, city, ip,
hostname, ip_org, timezone, country_iso2_code,
region_iso_code)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
%s, %s, %s)
"""

    # Values to insert
    values = (
        user_id,
        user_source,
        start,
        geo_data["latitude"],
        geo_data["longitude"],
        geo_data["postal"],
        geo_data["city"],
        geo_data["ip"],
        geo_data["hostname"],
        geo_data["ip_org"],
        geo_data["timezone"],
        geo_data["country_iso2_code"],
        geo_data["region_iso_code"],
    )

    debug(f"Start session SQL: {sql}")

    # Create session in the database
    CURR.execute(sql, values)

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
