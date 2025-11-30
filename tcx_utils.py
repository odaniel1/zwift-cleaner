import re
import os
import shutil
import logging
import subprocess
from logger_config import setup_logger

# Initialize the logger
logger = logging.getLogger(__name__)

def fit_to_tcx(fit_path, tcx_path):
    """
    Converts a .fit file to .tcx format using the fittotcx tool.

    Parameters:
        fit_path (str): Path to the input .fit file.
        tcx_path (str): Path to save the output .tcx file.
    """

    logger.info(f"Converting {fit_path} to {tcx_path}")

    # Validate input file exists
    if not os.path.isfile(fit_path):
        logger.error(f"Input .fit file does not exist: {fit_path}")
        raise FileNotFoundError(f"Input file not found: {fit_path}")
    
    # Validate output directory exists
    output_dir = os.path.dirname(tcx_path)
    if output_dir and not os.path.isdir(output_dir):
        logger.error(f"Output directory does not exist: {output_dir}")
        raise FileNotFoundError(f"Output directory not found: {output_dir}")

    # Define the command to run the tool
    command = ['fittotcx', fit_path]

    try:
        logger.info(f"Executing command: {' '.join(command)}")
        with open(tcx_path, 'w') as output_file:
            result = subprocess.run(
                command,
                stdout=output_file,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        logger.info(f"Conversion successful: {fit_path} -> {tcx_path}")
    except FileNotFoundError as e:
        logger.error(f"fittotcx. Ensure it is installed and in your PATH.")
        raise e
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with return code {e.returncode}")
        logger.error(f"Command stderr: {e.stderr.strip()}")
        raise RuntimeError(f"Conversion failed: {e.stderr.strip()}")
    except Exception as e:
        logger.exception("An unexpected error occurred during conversion.")
        raise RuntimeError(f"An unexpected error occurred: {e}")

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
    
def process_files_for_date(fit_files, date, temp_dir):
    """
    Converts .fit files to .tcx, merges them, and strips position data for a given date's files.
    Returns the path to the cleaned TCX file, or None if no files were processed.
    Args:
        fit_files (list): List of full paths to .fit files for the date.
        date (str): The date string (YYYY-MM-DD) for naming outputs.
        temp_dir (str): Path to the temporary directory for intermediate files.
    Returns:
        str: Path to the cleaned TCX file, or None if no files were processed.
    """
    temp_paths = []
    # Convert .fit to .tcx
    for fit_path in fit_files:
        tcx_filename = re.sub(r".fit$", ".tcx", os.path.basename(fit_path))
        tcx_path = os.path.join(temp_dir, tcx_filename)
        fit_to_tcx(fit_path, tcx_path)
        temp_paths.append(tcx_path)

    # Merge TCX files
    merged_path = os.path.join(temp_dir, f'merged_{date}.tcx')
    merge_tcx_files(temp_paths, merged_path)

    # Strip position data
    cleaned_path = os.path.join(temp_dir, f'cleaned_{date}.tcx')
    strip_position_from_tcx(merged_path, cleaned_path)

    return cleaned_path