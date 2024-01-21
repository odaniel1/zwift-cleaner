import functions_framework
from markupsafe import escape
import requests
import os

# [START functions_get_last_strava_activity]
@functions_framework.http
def get_last_strava_activity(request):
    access_token = os.environ.get('STRAVA_ACCESS_TOKEN')

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://www.strava.com/api/v3/athlete/activities', headers=headers)

    if response.status_code == 200:
        activities = response.json()
        if activities:
            last_activity = activities[0]  # Get the most recent activity
            return f'Last activity title: {last_activity["name"]}'
        else:
            return 'No activities found for this user.'
    else:
        return f'Error: Unable to fetch activities. Status code: {response.status_code}'
    
# [END functions_get_last_strava_activity]