import os
import logging
from logger_config import setup_logger
import webbrowser
from strava_auth import authorize_with_strava
from stravalib.client import Client
import constants

logger = logging.getLogger(__name__)

def open_activity_url(activity_id, url_path):
    activity_url = f'https://www.strava.com/activities/{activity_id}' 
    chrome_path = constants.chrome_path

    if os.path.exists(url_path):
        webbrowser.get(f'"{url_path}" %s').open(activity_url)
    else:
        logger.warning(f"No browserfound at {url_path}")