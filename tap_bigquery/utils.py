import logging, sys
from os import environ


LOGGER = None


def get_logger(name="handoff"):
    global LOGGER
    if not LOGGER:
        logging.basicConfig(
            stream=sys.stdout,
            format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
            level=logging.INFO,
        )
        LOGGER = logging.getLogger(name)
    return LOGGER


def get_service_account_credentials():
    return {
        "project_id": environ.get("GOOGLE_APPLICATION_SERVICE_ACCOUNT_PROJECT_ID"),
        "private_key": environ.get(
            "GOOGLE_APPLICATION_SERVICE_ACCOUNT_PRIVATE_KEY"
        ).replace("\\n", "\n"),
        "client_email": environ.get("GOOGLE_APPLICATION_SERVICE_ACCOUNT_CLIENT_EMAIL"),
        "token_uri": "https://oauth2.googleapis.com/token",
    }
