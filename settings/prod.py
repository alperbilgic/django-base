from settings.base import *

DEBUG = False
INSTALLED_APPS += (
    # other apps for production site
)

ALLOWED_HOSTS += []

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "https://www.myapp.com",
    "https://myapp-admin.vercel.app",
]

SECRET_KEY = os.environ.get("SECRET_KEY")

SIMPLE_JWT["SIGNING_KEY"] = os.environ.get("SECRET_KEY")
