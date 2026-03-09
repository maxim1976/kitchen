import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')

    # Railway injects postgres://, SQLAlchemy 1.4+ needs postgresql://
    _db_url = os.environ.get('DATABASE_URL', 'sqlite:///menu.db')
    SQLALCHEMY_DATABASE_URI = (
        _db_url.replace('postgres://', 'postgresql://', 1)
        if _db_url.startswith('postgres://')
        else _db_url
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'changeme')

    ESTIMATED_WAIT = int(os.environ.get('ESTIMATED_WAIT', '15'))  # minutes
