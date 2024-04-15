from settings.base import *

INSTALLED_APPS += (
    # other apps for production site
)

ALLOWED_HOSTS += ["myapp-test-ad7be68648ce.herokuapp.com"]

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://localhost:3000",
]

SECRET_KEY = os.environ.get("SECRET_KEY")

SIMPLE_JWT["SIGNING_KEY"] = os.environ.get("SECRET_KEY")
