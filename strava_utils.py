import json
import os
import logging
import webbrowser
from stravalib.client import Client
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from constants import CLIENT_ID, CLIENT_SECRET

# Initialize the logger
logger = logging.getLogger(__name__)

TOKEN_FILE = "strava_tokens.json"

# Step 1: Get authorization code via browser
class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        self.server.auth_code = query.get('code', [None])[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Success! You can close this window.")
    
    def log_message(self, format, *args):
        pass

def get_auth_code():
    client = Client()
    auth_url = client.authorization_url(
        client_id=CLIENT_ID,
        redirect_uri="http://localhost:8000",
        scope=["activity:write", "activity:read_all"]
    )
    print(f"\nOpen this URL in your browser:\n{auth_url}\n")
    
    try:
        import webbrowser
        webbrowser.open(auth_url)
    except:
        pass
    
    server = HTTPServer(('localhost', 8000), CallbackHandler)
    server.auth_code = None
    server.handle_request()
    return server.auth_code

# Step 2: Get authenticated client
def get_client():
    client = Client()
    
    try:
        # Try to use existing tokens
        with open(TOKEN_FILE) as f:
            tokens = json.load(f)
        
        # Refresh the access token
        new_tokens = client.refresh_access_token(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            refresh_token=tokens['refresh_token']
        )
        
        # Save refreshed tokens
        with open(TOKEN_FILE, 'w') as f:
            json.dump(new_tokens, f)
        
        client.access_token = new_tokens['access_token']
        
    except FileNotFoundError:
        # First time - do full OAuth flow
        code = get_auth_code()
        tokens = client.exchange_code_for_token(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            code=code
        )
        
        # Save tokens
        with open(TOKEN_FILE, 'w') as f:
            json.dump(tokens, f)
        
        client.access_token = tokens['access_token']
    
    return client

# Step 3: Upload TCX file
def upload_tcx(client, tcx_file_path, name="Uploaded Activity", activity_type="ride", trainer=False):
    with open(tcx_file_path, 'r') as f:
        upload = client.upload_activity(
            activity_file=f,
            data_type='tcx',
            name=name,
            activity_type=activity_type
        )

        activity = upload.wait()
        logger.info(f"Activity created, activity_id: {activity.id}")
    return activity      

def open_activity_url(activity_id, url_path):
    activity_url = f'https://www.strava.com/activities/{activity_id}' 

    if os.path.exists(url_path):
        webbrowser.get(f'"{url_path}" %s').open(activity_url)
    else:
        logger.warning(f"No browserfound at {url_path}")