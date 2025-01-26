import os
import re
import sys
import logging
import tempfile
import time
from datetime import datetime
from logger_config import setup_logger
from get_matching_files import get_matching_files
from fit_to_tcx import fit_to_tcx
from merge_tcx_files import merge_tcx_files
from strip_position_from_tcx import strip_position_from_tcx
from strava_auth import authorize_with_strava
from strava_write import write_to_strava
from strava_open import get_latest_activity_id, open_activity_url
import constants

# Initialize logging
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting TCX processing and upload workflow.")

    """
    Main function to process and upload TCX files to Strava.
    """
    try:
        # Define paths and patterns
        zwift_path = constants.zwift_path
        today = datetime.today().strftime('%Y-%m-%d')

        # Get today's fit files; excluding files smaller than 5kb
        todays_fit_files = get_matching_files(zwift_path, today + ".*", 5 * 1024)

        # Stop if there are no files
        if len(todays_fit_files) == 0:
            logger.error(f"No valid fit files in {zwift_path}")
            sys.exit(1)

        # Process files in a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_paths = []

            # Convert .fit to .tcx
            for fit_file in todays_fit_files:
                fit_path = os.path.join(zwift_path, fit_file)
                tcx_path = os.path.join(temp_dir, re.sub(r".fit$", ".tcx", fit_file))
                fit_to_tcx(fit_path, tcx_path)
                temp_paths.append(tcx_path)

            # Merge TCX files
            merged_path = os.path.join(temp_dir, 'merged.tcx')
            merge_tcx_files(temp_paths, merged_path)
            
            # Strip position data
            cleaned_path = os.path.join(temp_dir, 'cleaned.tcx')
            strip_position_from_tcx(merged_path, cleaned_path)
            
            # Authorize with Strava
            access_token = authorize_with_strava()

            # Upload to Strava
            upload = write_to_strava(cleaned_path, access_token)
            if upload:
                logger.info(f"Upload successful! Activity ID: {upload.upload_id}")
            else:
                logger.error("Failed to upload activity to Strava.")
            
            # Open url of new activity
            time.sleep(5)
            activity_id = get_latest_activity_id(access_token)
            open_activity_url(activity_id, constants.chrome_path)
            #athlete_id = get_athlete_id(access_token)
            #open_strava_profile(athlete_id, constants.chrome_path)

    except Exception as e:
        logger.exception("An unexpected error occurred in the workflow.")

    logger.info("Workflow completed.")
