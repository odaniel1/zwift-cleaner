import sys
import logging
import tempfile
from date_utils import parse_dates_from_args
from file_utils import get_matching_files
from tcx_utils import process_files_for_date
from strava_utils import get_client, upload_tcx, open_activity_url
import constants

# Initialize logging
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting TCX processing and upload workflow.")

    """
    Main function to process and upload TCX files to Strava.
    Accepts one or more dates as command line arguments (YYYY-MM-DD ...).
    If no dates are provided, uses today's date.
    """
    try:
        # Define constants and get access token once.
        date_list = parse_dates_from_args(sys.argv, logger)
        zwift_path = constants.zwift_path
        strava_client = get_client()

        for target_date in date_list:
            logger.info(f"Processing date: {target_date}")

            # Get fit files for target date; excluding files smaller than 5kb
            date_fit_files = get_matching_files(zwift_path, target_date + ".*", 5 * 1024)

            # If there are no valid files, continue to the next date
            if not date_fit_files:
                logger.warning(f"No valid fit files found for {target_date}. Skipping.")
                continue

            # Process files in a temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                date_tcx_processed = process_files_for_date(date_fit_files, target_date, temp_dir) 

                # Upload to Strava
                activity = upload_tcx(strava_client, date_tcx_processed, name="Turbo Session", activity_type="ride", trainer=True)

                # Open the new activity in browser
                open_activity_url(activity.id, constants.chrome_path)

    except Exception as e:
        logger.exception("An unexpected error occurred in the workflow.")

    logger.info("Workflow completed.")
