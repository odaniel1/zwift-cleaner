
# zwift-cleaner
Clean Zwift '.fit' files for a happy Strava feed.

Zwift cleaner processes locally held `.fit` files, stripping them of their location data before pushing them to your Strava feed.

When `main.py` is run, the following workflow is executed:

1. Any `.fit` files within your Zwift `/Activities` folder which match today's date are converted to `.tcx` files and saved as temporary files.

2. If there are more than one matched file, files are combined into a single activity.

3. Latitude and longitude data are stripped from the combined activity.

4. Authentication with Strava is made, and the resulting `.tcx` file is uploaded to the associated Strava account with the title 'Turbo Session'.

As a user - when running this script a browser window will open asking you to confirm that you are happy for the App to write to Strava.

## Setup
### Package management
Required packages are listed in `requirements.txt`.
Note that the `fit-to-tcx` package needs to be installed from [this](https://github.com/odaniel1/FIT-to-TCX) fork, which has been updated to ensure that power data is not disregarded.

### Strava App
You will need to have a [Strava app](https://developers.strava.com/) associated with your account.

### Secret management
In your local project you need to create a file called `constants.py`. This should have the following contents:

```
CLIENT_ID = '<your strava client id>'
CLIENT_SECRET = '<your strava client secret>'
zwift_path = '<path to your zwift Activities folder>'
```

### Browser
During the authentication of the Strava app, a browser window will open asking for authorisation for the app to write files to Strava.

This is currently set-up to open in Chrome, and assumes that you have Chrome on your machine.