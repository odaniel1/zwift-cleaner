import subprocess
import os
import logging
from logger_config import setup_logger

# Get a logger for this module
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