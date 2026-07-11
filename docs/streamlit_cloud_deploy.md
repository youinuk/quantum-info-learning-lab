# Streamlit Community Cloud Deployment

## Python version

Use Python 3.12 for the Streamlit Cloud app.

The app was observed failing on Streamlit Community Cloud when the runtime was
Python 3.14.6. The dependency installation completed, but the Streamlit process
ended with a segmentation fault before app code could render.

In Streamlit Community Cloud:

1. Open the app settings.
2. Open Advanced settings.
3. Set Python version to Python 3.12.
4. Reboot or redeploy the app.

`runtime.txt` is included as a repository hint, but Streamlit Community Cloud's
current documented control is the Python version dropdown in Advanced settings.

## Dependencies

`requirements.txt` intentionally avoids very wide upper ranges. This keeps Cloud
from resolving to the newest Python 3.14-oriented binary stack when the app is
intended to run on Python 3.12.

After changing dependencies or Python version, check the Cloud logs for:

- Python version should be 3.12.x.
- Dependencies should install from `requirements.txt`.
- The app should proceed past `Uvicorn server started` without a segmentation fault.
