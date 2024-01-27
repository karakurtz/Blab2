import os

PROPAGATE_EXCEPTIONS = True
FLASK_DEBUG = True

# Database Configuration
SQLALCHEMY_DATABASE_URI = f"{os.environ['POSTGRES_NAME']}://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}/{os.environ['POSTGRES_DB']}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

