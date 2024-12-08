import threading
import webbrowser
import os
import logging
from logger_config import setup_logger
from flask import Flask, request
from stravalib.client import Client
import constants

# Initialize the logger
logger = logging.getLogger(__name__)

# Strava API client configuration
CLIENT_ID = constants.CLIENT_ID
CLIENT_SECRET = constants.CLIENT_SECRET
REDIRECT_URI = 'http://localhost:5000/callback'  # Flask will listen on this URI

# Flask app
app = Flask(__name__)

# Strava client
client = Client()

# Shared variable for authorization token (managed via threading)
class AuthorizationState:
    def __init__(self):
        self.token = None
        self.lock = threading.Condition()

auth_state = AuthorizationState()

@app.route('/callback')
def callback():
    """
    Handle the redirect from Strava and extract the authorization code.
    """
    authorization_code = request.args.get('code')
    if not authorization_code:
        logger.error("No authorization code provided.")
        return "Authorization failed or no code provided.", 400

    try:
        # Exchange the authorization code for an access token
        token_response = client.exchange_code_for_token(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            code=authorization_code
        )
        with auth_state.lock:
            auth_state.token = token_response['access_token']
            auth_state.lock.notify()

        logger.info("Authorization successful. Access token obtained.")
        return "Authorization successful! You can close this page.", 200
    except Exception as e:
        logger.exception("Failed to exchange authorization code for access token.")
        return f"Authorization failed: {e}", 500


def run_flask():
    """
    Run the Flask app in a separate thread.
    """
    try:
        logger.info("Starting Flask server.")
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        logger.exception("Error occurred while starting the Flask server.")


def stop_flask(server_thread):
    """
    Stop the Flask app by terminating its thread.
    """
    if server_thread and server_thread.is_alive():
        logger.info("Stopping Flask server.")
        server_thread.join(timeout=1)


def authorize_with_strava():
    """
    Runs the Strava authorization workflow.

    Returns:
        str: The access token obtained from the authorization process.
    """
    # Generate the authorization URL
    try:
        authorize_url = client.authorization_url(
            client_id=CLIENT_ID,
            redirect_uri=REDIRECT_URI,
            scope=['activity:write']
        )
        logger.info(f"Generated Strava authorization URL: {authorize_url}")

        # Open the authorization URL in Chrome
        chrome_path = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
        if os.path.exists(chrome_path):
            logger.info("Opening authorization URL in Chrome.")
            webbrowser.get(f'"{chrome_path}" %s').open(authorize_url)
        else:
            logger.warning(f"Chrome not found at {chrome_path}. Please open the URL manually: {authorize_url}")
    except Exception as e:
        logger.exception("Failed to generate or open the authorization URL.")
        return None

    # Start the Flask app in a separate thread
    server_thread = threading.Thread(target=run_flask, daemon=True)
    server_thread.start()

    # Wait for the authorization token
    with auth_state.lock:
        while not auth_state.token:
            logger.info("Waiting for user authorization...")
            auth_state.lock.wait(timeout=5)

    # Stop the Flask server
    stop_flask(server_thread)

    return auth_state.token
