# zwift-cleaner

<p align="center">
  <img src="zwift-cleaner.png" alt="zwift-cleaner" width="256">
</p>

Tired of Zwift rides cluttering your Strava feed with routes that appear in far‑off places? `zwift-cleaner` is a Windows utility that automatically cleans and uploads your Zwift activities to Strava, removing location data for privacy and a tidier feed.

The typical workflow is driven by the `run_zwift_and_clean.bat` script, which launches Zwift and then calls the Python code in `main.py` to process your latest activities. Under the hood, the tool:

1. Finds all `.fit` files in your Zwift `/Activities` folder that match today's date.
2. Converts these `.fit` files to `.tcx` format and, if multiple files are found, combines them into a single activity.
3. Strips all latitude and longitude data from the combined activity file.
4. Authenticates with Strava and uploads the cleaned `.tcx` file to your account with the title `Turbo Session`.

When the upload step runs for the first time, a browser window will open asking you to authorize the app to write activities to your Strava account.

## Setup
### Package management
Required packages are listed in `requirements.txt`.
Note that the `fit-to-tcx` package needs to be installed from [this](https://github.com/odaniel1/FIT-to-TCX) fork, which has been updated to ensure that power data is not disregarded.

### Strava App
You will need to have a [Strava app](https://developers.strava.com/) associated with your account.

### Secret management
In your local project directory you need a `constants.py` file, which is **not** committed to source control. It should define your Zwift paths and Strava app credentials:

```python
# zwift paths
ZWIFT_ACTIVITIES_PATH = "<path to your Zwift folder where activities are stored>"
ZWIFT_EXECUTABLE_PATH = "<path to your Zwift executable>"

# Strava app secrets
CLIENT_ID = "<your Strava app client ID>"
CLIENT_SECRET = "<your Strava app client secret>"
```