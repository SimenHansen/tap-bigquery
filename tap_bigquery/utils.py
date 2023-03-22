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
        "type": environ.get("GOOGLE_APPLICATION_SERVICE_ACCOUNT_TYPE"),
        "project_id": environ.get("GOOGLE_APPLICATION_SERVICE_ACCOUNT_TYPE"),
        "private_key_id": environ.get(
            "GOOGLE_APPLICATION_SERVICE_ACCOUNT_PRIVATE_KEY_ID"
        ),
        "private_key": environ.get("GOOGLE_APPLICATION_SERVICE_ACCOUNT_PRIVATE_KEY"),
        "client_email": environ.get("GOOGLE_APPLICATION_SERVICE_ACCOUNT_CLIENT_EMAIL"),
        "client_id": environ.get("GOOGLE_APPLICATION_SERVICE_ACCOUNT_CLIENT_ID"),
        "auth_uri": environ.get("GOOGLE_APPLICATION_SERVICE_ACCOUNT_AUTH_URI"),
        "token_uri": environ.get("GOOGLE_APPLICATION_SERVICE_ACCOUNT_TOKEN_URI"),
        "auth_provider_x509_cert_url": environ.get(
            "GOOGLE_APPLICATION_SERVICE_ACCOUNT_AUTH_PROVIDER_X509"
        ),
        "client_x509_cert_url": environ.get(
            "GOOGLE_APPLICATION_SERVICE_ACCOUNT_CLIENT_X509"
        ),
    }
