import os
import re
import logging
from logger_config import setup_logger

# Get a logger for this module
logger = logging.getLogger(__name__)

def get_matching_files(directory_path, pattern, min_size = None):
    """
    Returns a list of files in the specified directory that match the given regular expression pattern.

    Parameters:
        directory_path (str): The path to the directory to search.
        pattern (str): The regular expression pattern to match file names.

    Returns:
        List: A sorted list of file names that match the pattern.
    """
    logger.info(f"Looking for fit files in {directory_path} matching pattern: {pattern}")

    try:
        # Validate that the directory exists
        if not os.path.isdir(directory_path):
            logging.error(f"The directory '{directory_path}' does not exist.")
            return []

        # Compile the regular expression
        try:
            regex = re.compile(pattern)
        except re.error as e:
            logging.error(f"Invalid regular expression pattern: {e}")
            return []

        # Get all files in the specified directory
        files = os.listdir(directory_path)
        logging.info(f"Found {len(files)} files in directory '{directory_path}'.")

        # Filter files based on the regular expression pattern
        matching_files = [f for f in files if regex.fullmatch(f)]
        logger.info(f"Found {len(matching_files)} fit file(s): {matching_files}")

        if min_size == None:
            return sorted(matching_files)
        else:
            # Filter files to remove files smaller than min_size
            big_files = [f for f in matching_files if os.path.getsize(directory_path + '/' + f) > min_size]
            logger.info(f"Found {len(big_files)} fit file(s) larger than {min_size} bytes: {big_files}")
            return sorted(big_files)
    
    except PermissionError:
        logging.error(f"Permission denied for directory '{directory_path}'.")
        return []
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        return []