
# zwift-cleaner
Clean Zwift '.fit' files for a happy Strava feed.

## Getting Started with Cloud Functions
Basic project agnostic set-up is well documented by Google in [this](https://cloud.google.com/functions/docs/tutorials/http) tutorial, which is specifically targeted at using Google Cloud Functions from a local command line environment (as opposed to developing cloud functions from the GCP Console).

Assuming you have followed steps in the section *Before you begin*. At this point you should have:
* Created a project in the Google Cloud console, with billing  and the appropriate API's enabled.
* Installed the Google Cloud CLI locally, and initialised it.
* Created a python virtual environment for the project.

::1:: Ensure you have the required package dependencies installed in your python environment.

Option A: if following these instructions for the specific `zwift-cleaner` workflow then install the packages from `requirements.txt`.

```
pip install -r requirements. txt
```

Option B: if you happen to be reading this as a generic into to deploying cloud functions, then install `functions-framework` and then write/update your `requirements.txt`.

```
pip install functions-framework
pip freeze > requirements.txt
```

::2:: Initialise the gcloud CLI, and follow the steps to activate the correct project and choose your region.

```
gcloud init
```

```
gcloud auth application-default login
```

::3:: Follow the steps in [this](https://jessicasalbert.medium.com/holding-your-hand-through-stravas-api-e642d15695f2) blog to set-up a Strava API connected to your Strava account.

::4:: Deploy your cloud function (in this case `get_last_strava_activity`), the `region` argument should be the region you set in the initialisation step above (in my case I've chosen to use `europe-west1`), and the text `SECRET_TOKEN` for your Strava app.

In this deployment the `no-allow-unauthenticated` argument will ensure that only authorised users can call the deployed function.

```
gcloud functions deploy get_last_strava_activity \
--gen2 \
--runtime=python311 \
--region=europe-west1 \
--source=. \
--entry-point=get_last_strava_activity \
--trigger-http \
--no-allow-unauthenticated \
--update-env-vars STRAVA_ACCESS_TOKEN=SECRET_TOKEN
```

::5:: Check the function, replacing `URI` with the URI that was returned from the above command. This should return the title of your last Strava activity.

```
curl -m 70 -X POST URI \
    -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
    -H "Content-Type: application/json" \
    -d '{}'
```

