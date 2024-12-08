import logging

# Configure logging
def setup_logger():
    logging.basicConfig(
        level=logging.INFO,  # Default log level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("zwift_cleaner.log"),  # Logs to a file
            logging.StreamHandler()         # Logs to console
        ]
    )
    logging.info("Logger is configured")

# Call this function once, in the main entry point
setup_logger()
