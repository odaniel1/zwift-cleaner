import os
import logging
from logger_config import setup_logger
import webbrowser
from strava_auth import authorize_with_strava
from stravalib.client import Client
import constants

logger = logging.getLogger(__name__)

def get_latest_activity_id(access_token):
    """
    Runs the Strava authorization workflow.

    Returns:
        str: The access token obtained from the authorization process.
    """
    
    client = Client()
    client.access_token = access_token
    logger.info("Strava client initialized with access token.")
    
    # Retrieve the latest activity
    activities = client.get_activities(limit=1)
    latest_activity = next(activities)
    activity_id = latest_activity.id

    return activity_id

def get_athlete_id(access_token):
    """
    Runs the Strava authorization workflow.

    Returns:
        str: The access token obtained from the authorization process.
    """
    
    client = Client()
    client.access_token = access_token
    logger.info("Strava client initialized with access token.")
    
    # Retrieve the latest activity
    athlete = client.get_athlete()
    athlete_id = athlete.id
    print(f"\n\n --- Logged in as athlete id:{athlete_id} --- \n\n")
    return athlete_id

def open_activity_url(activity_id, url_path):
    activity_url = f'https://www.strava.com/activities/{activity_id}' 
    chrome_path = constants.chrome_path

    if os.path.exists(url_path):
        webbrowser.get(f'"{url_path}" %s').open(activity_url)
    else:
        logger.warning(f"No browserfound at {url_path}")

def open_strava_profile(athlete_id, url_path):
    user_url = f'https://www.strava.com/athletes/{athlete_id}'
    chrome_path = constants.chrome_path

    if os.path.exists(url_path):
        webbrowser.get(f'"{url_path}" %s').open(user_url)
    else:
        logger.warning(f"No browserfound at {url_path}")