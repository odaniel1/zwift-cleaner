import re
import os
import shutil
import logging
from logger_config import setup_logger

# Initialize the logger
logger = logging.getLogger(__name__)

def merge_tcx_files(tcx_paths, output_path):
    """
    Merges multiple TCX files into one by combining their <Lap> elements.

    Parameters:
        tcx_paths (list): List of paths to the input TCX files.
        output_path (str): Path to the output merged TCX file.

    Returns:
        str: A message indicating the result of the merge operation.
    """
    logger.info("Starting TCX file merge.")
    logger.debug(f"Input files: {tcx_paths}")
    logger.debug(f"Output path: {output_path}")

    # Validate input paths
    if not tcx_paths or not isinstance(tcx_paths, list):
        logger.error("No valid input paths provided.")
        return 'Error: No paths provided.'
    
    # Validate that all input paths are valid
    if not all(os.path.isfile(path) for path in tcx_paths):
        logger.error("One or more input paths are invalid.")
        return 'Error: One or more input files do not exist.'

    # Validate output directory
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.isdir(output_dir):
        logger.error("Output directory does not exist.")
        return 'Error: Output directory is invalid.'

    n_paths = len(tcx_paths)

    if n_paths == 0:
        logger.error("Empty input paths list.")
        return 'Error: No paths provided.'

    if n_paths == 1:
            logger.info("Only one TCX file provided. No merge required.")
            shutil.copy(tcx_paths[0], output_path)
            logger.info(f"Copied file to {output_path}")
            return f'File written to {output_path}'
    
    # Regex patterns for extracting relevant parts of the TCX content
    pre_lap_pattern = r'^.*?(<Lap)'
    after_lap_pattern = r'(.*</Lap>).*'

    try:
        # Read the content of the first TCX file
        with open(tcx_paths[0], 'r', encoding='utf-8') as file:
            content = file.read()

        # Remove the 'tail' of the first TCX file
        merged_content = re.sub(after_lap_pattern, r'\1', content, flags=re.DOTALL)

        # Merge additional TCX files
        for n, path in enumerate(tcx_paths[1:], start=2):
            logger.debug(f"Processing file {n}: {path}")
            with open(path, 'r', encoding='utf-8') as file:
                new_content = file.read()

            # Remove the 'head' of the TCX file
            new_content = re.sub(pre_lap_pattern, r'\1', new_content, flags=re.DOTALL)

            if n < n_paths:
                # Remove the 'tail' of the TCX file
                new_content = re.sub(after_lap_pattern, r'\1', new_content, flags=re.DOTALL)

            merged_content += new_content

        # Write merged content to the output file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(merged_content)

        logger.info(f"Merge complete. File written to {output_path}")
        return f'File written to {output_path}'

    except Exception as e:
        logger.exception("An error occurred during the merge process.")
        return f'Error: {e}'