import re
import os
import logging
from logger_config import setup_logger

# Initialize the logger
logger = logging.getLogger(__name__)

def strip_position_from_tcx(tcx_path, output_path):
    """
    Removes <Position> elements from a TCX file.

    Parameters:
        tcx_path (str): Path to the input TCX file.
        output_path (str): Path to save the modified TCX file.

    Returns:
        str: Message indicating the result of the operation.
    """
    logger.info(f"Starting to strip position data from {tcx_path}.")
    
    # Validate input file
    if not os.path.isfile(tcx_path):
        logger.error(f"Input file does not exist: {tcx_path}")
        return f"Error: File not found: {tcx_path}"
    
    # Validate output directory
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.isdir(output_dir):
        logger.error(f"Output directory does not exist: {output_dir}")
        return f"Error: Output directory does not exist: {output_dir}"
    
    try:
        # Read the content of the TCX file
        with open(tcx_path, 'r', encoding='utf-8') as file:
            content = file.read()
        logger.debug("Successfully read input file.")

        # Define the regex pattern to match <Position> tags
        pattern = re.compile(r'<Position>.*?</Position>\s*', re.DOTALL)
        logger.debug(f"Regex pattern used: {pattern.pattern}")

        # Remove <Position> tags and their content
        modified_content = re.sub(pattern, '', content)
        logger.debug("Successfully stripped position data.")

        # Write the modified content to the output file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        logger.info(f"Position data stripped successfully. Output saved to {output_path}")

        return f"Position data stripped successfully. Output saved to {output_path}"

    except FileNotFoundError:
        logger.error(f"File not found: {tcx_path}")
        return f"Error: File not found: {tcx_path}"
    except PermissionError:
        logger.error(f"Permission denied for file: {tcx_path} or {output_path}")
        return f"Error: Permission denied for file: {tcx_path} or {output_path}"
    except Exception as e:
        logger.exception("An unexpected error occurred.")
        return f"Error: An unexpected error occurred: {e}"
