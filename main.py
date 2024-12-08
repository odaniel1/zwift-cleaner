from get_matching_files import get_matching_files
from fit_to_tcx import fit_to_tcx
from merge_tcx_files import merge_tcx_files
from strip_position_from_tcx import strip_position_from_tcx
from datetime import datetime
from strava_auth import authorize_with_strava
from strava_write import write_to_strava
from stravalib.client import Client
import constants
import tempfile
import re
import os

zwift_path = constants.zwift_path
today = datetime.today().strftime('%Y-%m-%d')

todays_fit_files = get_matching_files(zwift_path, today + ".*")

with tempfile.TemporaryDirectory() as temp_dir:
    temp_paths = []

    for f in todays_fit_files:
        fit_path = os.path.join(zwift_path,f)
        tcx_path = os.path.join(temp_dir,re.sub(".fit",".tcx", f))

        fit_to_tcx(fit_path, tcx_path)

        temp_paths.append(tcx_path)
    
    merged_path = os.path.join(temp_dir, 'merged.tcx')
    merge_tcx_files(temp_paths, merged_path)
    
    cleaned_path = os.path.join(temp_dir, 'cleaned.tcx')
    
    strip_position_from_tcx(merged_path, cleaned_path)
   
    access_token = authorize_with_strava()
    client = Client()
    write_to_strava(cleaned_path, access_token) 