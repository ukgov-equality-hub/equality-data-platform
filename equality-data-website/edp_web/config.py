import logging
import os
from os.path import dirname


class Config:
    BASE_DIRECTORY = dirname(dirname(os.path.abspath(__file__)))
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "PRODUCTION")
    LOG_LEVEL = (
        logging.getLevelName(os.environ.get("LOG_LEVEL"))
        if "LOG_LEVEL" in os.environ
        else logging.INFO
    )
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # Stops the CSRF token expiring (before the lifetime of the session). This was an accessibility problem
    MAINTENANCE_MODE = os.environ.get("MAINTENANCE_MODE")
    BASIC_AUTH_USERNAME = os.environ.get("BASIC_AUTH_USERNAME")
    BASIC_AUTH_PASSWORD = os.environ.get("BASIC_AUTH_PASSWORD")
    ENTERPRISE_TASKFORCE_S3_BUCKET = os.environ.get("ENTERPRISE_TASKFORCE_S3_BUCKET")
    ENTERPRISE_TASKFORCE_PASSWORD = os.environ.get("ENTERPRISE_TASKFORCE_PASSWORD")
    ENTERPRISE_TASKFORCE_2_S3_BUCKET = os.environ.get("ENTERPRISE_TASKFORCE_2_S3_BUCKET")
    ENTERPRISE_TASKFORCE_2_PASSWORD = os.environ.get("ENTERPRISE_TASKFORCE_2_PASSWORD")


class DevConfig(Config):
    DEBUG = True
    ENVIRONMENT = "DEVELOPMENT"
    LOG_LEVEL = (
        logging.getLevelName(os.environ.get("LOG_LEVEL"))
        if "LOG_LEVEL" in os.environ
        else logging.DEBUG
    )
    # SERVER_NAME = "localhost:5000"


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
