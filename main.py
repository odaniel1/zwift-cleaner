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

        # Handle command line argument for target_date
        if len(sys.argv) == 1:
            target_date = datetime.today().strftime('%Y-%m-%d')
            logger.info(f"No date argument provided. Using today's date: {target_date} as default.")
        elif len(sys.argv) == 2:
            arg_date = sys.argv[1]
            if re.match(r"^\d{4}-\d{2}-\d{2}$", arg_date):
                try:
                    # Try to parse the date to ensure it's valid
                    datetime.strptime(arg_date, "%Y-%m-%d")
                    target_date = arg_date
                    logger.info(f"Using provided date argument: {target_date}")
                except ValueError:
                    logger.error("Invalid date value. Please provide a valid date in YYYY-MM-DD format.")
                    sys.exit(1)
            else:
                logger.error("Invalid date argument. Please provide date in YYYY-MM-DD format or omit for today's date.")
                sys.exit(1)
        else:
            logger.error("Too many arguments. Please provide only one date argument in YYYY-MM-DD format or omit for today's date.")
            sys.exit(1)

        # Get fit files for target date; excluding files smaller than 5kb
        fit_files = get_matching_files(zwift_path, target_date + ".*", 5 * 1024)

        # Stop if there are no files
        if len(fit_files) == 0:
            logger.error(f"No valid fit files in {zwift_path}")
            sys.exit(1)

        # Process files in a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_paths = []

            # Convert .fit to .tcx
            for f in fit_files:
                fit_path = os.path.join(zwift_path, f)
                tcx_path = os.path.join(temp_dir, re.sub(r".fit$", ".tcx", f))
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
            activity = write_to_strava(cleaned_path, access_token)

            # Open the new activity in browser
            open_activity_url(activity.id, constants.chrome_path)

    except Exception as e:
        logger.exception("An unexpected error occurred in the workflow.")

    logger.info("Workflow completed.")
