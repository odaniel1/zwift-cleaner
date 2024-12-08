import os
import re
import logging
import tempfile
from datetime import datetime
from logger_config import setup_logger
from get_matching_files import get_matching_files
from fit_to_tcx import fit_to_tcx
from merge_tcx_files import merge_tcx_files
from strip_position_from_tcx import strip_position_from_tcx
from strava_auth import authorize_with_strava
from strava_write import write_to_strava
import constants

# Initialize logging
logger = logging.getLogger(__name__)

def process_and_upload_tcx_files():
    """
    Main function to process and upload TCX files to Strava.
    """
    try:
        # Define paths and patterns
        zwift_path = constants.zwift_path
        today = datetime.today().strftime('%Y-%m-%d')

        # Get today's fit files
        logger.info(f"Looking for fit files in {zwift_path} for date pattern: {today}")
        todays_fit_files = get_matching_files(zwift_path, today + ".*")
        if not todays_fit_files:
            logger.warning("No fit files found for today's date.")
            return

        logger.info(f"Found {len(todays_fit_files)} fit file(s): {todays_fit_files}")

        # Process files in a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_paths = []

            # Convert .fit to .tcx
            for fit_file in todays_fit_files:
                fit_path = os.path.join(zwift_path, fit_file)
                tcx_path = os.path.join(temp_dir, re.sub(r".fit$", ".tcx", fit_file))

                logger.info(f"Converting {fit_path} to {tcx_path}")
                try:
                    fit_to_tcx(fit_path, tcx_path)
                    temp_paths.append(tcx_path)
                except Exception as e:
                    logger.exception(f"Failed to convert {fit_path} to TCX.")
                    continue

            if not temp_paths:
                logger.error("No TCX files were successfully generated.")
                return

            # Merge TCX files
            merged_path = os.path.join(temp_dir, 'merged.tcx')
            logger.info(f"Merging TCX files into {merged_path}")
            try:
                merge_tcx_files(temp_paths, merged_path)
            except Exception as e:
                logger.exception("Failed to merge TCX files.")
                return

            # Strip position data
            cleaned_path = os.path.join(temp_dir, 'cleaned.tcx')
            logger.info(f"Stripping position data from {merged_path} to {cleaned_path}")
            try:
                strip_position_from_tcx(merged_path, cleaned_path)
            except Exception as e:
                logger.exception("Failed to clean TCX file.")
                return

            # Authorize with Strava
            logger.info("Authorizing with Strava.")
            try:
                access_token = authorize_with_strava()
                if not access_token:
                    logger.error("Authorization with Strava failed.")
                    return
            except Exception as e:
                logger.exception("Failed to authorize with Strava.")
                return

            # Upload to Strava
            logger.info(f"Uploading {cleaned_path} to Strava.")
            try:
                upload = write_to_strava(cleaned_path, access_token)
                if upload:
                    logger.info(f"Upload successful! Activity ID: {upload.upload_id}")
                else:
                    logger.error("Failed to upload activity to Strava.")
            except Exception as e:
                logger.exception("Failed to upload activity to Strava.")
    except Exception as e:
        logger.exception("An unexpected error occurred in the workflow.")


if __name__ == "__main__":
    logger.info("Starting TCX processing and upload workflow.")
    process_and_upload_tcx_files()
    logger.info("Workflow completed.")
