from settings.base import *

INSTALLED_APPS += (
    # other apps for production site
)

ALLOWED_HOSTS += ["localhost", "127.0.0.1", "[::1]", "*"]

if DATABASES["default"] == {}:
    DATABASES["default"] = dj_database_url.parse("postgresql://localhost:6666/myapp")

SIMPLE_JWT["SIGNING_KEY"] = SECRET_KEY

try:
    from settings.local_overrides import *
except:
    pass
