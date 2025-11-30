import os
import logging
from logger_config import setup_logger
import time
from strava_auth import authorize_with_strava
from stravalib.client import Client

# Initialize the logger
logger = logging.getLogger(__name__)

def write_to_strava(tcx_path, access_token, max_retries=10, retry_delay=1):
    """
    Uploads a TCX file to Strava as an activity.

    Parameters:
        tcx_path (str): Path to the TCX file to upload.
        access_token (str): Strava API access token.
        max_retries (int): Maximum number of retries for upload processing.
        retry_delay (int): Delay (in seconds) between retries.

    Returns:
        int: The activity ID if the upload is successful, None otherwise.
    """
    # Validate the TCX file
    if not os.path.isfile(tcx_path):
        logger.error(f"File not found: {tcx_path}")
        return None

    # Initialize the Strava client
    client = Client()
    client.access_token = access_token
    logger.info("Strava client initialized with access token.")

    try:
        # Upload the activity
        logger.info(f"Uploading activity from file: {tcx_path}")
        with open(tcx_path, 'rb') as tcx_file:
            upload = client.upload_activity(
                activity_file=tcx_file,
                data_type='tcx',
                name="Turbo Session",
                trainer=True
            )

            activity = upload.wait()
            logger.info(f"Activity created, activity_id: {activity.id}")
            return activity      
          
    except Exception as e:
        logger.exception("An error occurred during the upload process.")
        return None