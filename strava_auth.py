import threading
import webbrowser
import os
from flask import Flask, request
from stravalib.client import Client
import constants

# Strava API client configuration
CLIENT_ID = constants.CLIENT_ID
CLIENT_SECRET = constants.CLIENT_SECRET
REDIRECT_URI = 'http://localhost:5000/callback'  # Flask will listen on this URI

# Flask app
app = Flask(__name__)
authorization_token = None  # Global variable to store the token
server_thread = None         # Thread for the Flask server

# Strava client
client = Client()

@app.route('/callback')
def callback():
    """
    Handle the redirect from Strava and extract the authorization code.
    """
    global authorization_token
    authorization_code = request.args.get('code')
    if not authorization_code:
        return "Authorization failed or no code provided.", 400

    # Exchange the authorization code for an access token
    token_response = client.exchange_code_for_token(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        code=authorization_code
    )
    authorization_token = token_response['access_token']

    # Return a success response
    return "Authorization successful! You can close this page.", 200


def run_flask():
    """
    Run the Flask app in a separate thread.
    """
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)


def stop_flask():
    """
    Stop the Flask app by terminating its thread.
    """
    global server_thread
    if server_thread:
        server_thread.join(timeout=1)  # Wait for the thread to terminate


def authorize_with_strava():
    """
    Runs the Strava authorization workflow.
    """
    global authorization_token, server_thread

    # Generate the authorization URL
    authorize_url = client.authorization_url(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI, scope=['activity:write'])
    print(f"Opening the authorization URL: {authorize_url}")

    # Open the authorization URL in Chrome
    chrome_path = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
    if os.path.exists(chrome_path):
        webbrowser.get(f'"{chrome_path}" %s').open(authorize_url)
    else:
        print(f"Chrome not found at {chrome_path}. Please check the path or open the URL manually: {authorize_url}")

    # Start the Flask app in a separate thread
    server_thread = threading.Thread(target=run_flask, daemon=True)
    server_thread.start()

    # Wait for authorization token
    while not authorization_token:
        pass

    # Stop the Flask app
    stop_flask()

    return authorization_token