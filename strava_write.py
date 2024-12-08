from strava_auth import authorize_with_strava
from stravalib.client import Client
import time

def write_to_strava(tcx_path, access_token):
    client = Client()
    client.access_token = access_token

    # Upload the activity
    with open(tcx_path, 'rb') as tcx_file:
        upload = client.upload_activity(
            activity_file=tcx_file,
            data_type='tcx',
            name="Turbo Session",
            private = False,
            trainer = True
        )

    # Wait for the upload to process
    while not upload.is_processing and not upload.activity_id:
        time.sleep(1)
        upload = client.get_upload(upload.id)

    if upload.activity_id:
        print(f'Upload successful! Activity ID: {upload.activity_id}')
    else:
        print(f'Upload failed: {upload.error}')