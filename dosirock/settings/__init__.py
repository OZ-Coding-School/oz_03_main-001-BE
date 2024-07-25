import os

from dotenv import load_dotenv


load_dotenv()

ENVIRONMENT = os.getenv("DJANGO_ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    from .production import *
elif ENVIRONMENT == "development":
    from .local import *
