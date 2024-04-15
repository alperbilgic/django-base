from utils.constants.environment_variables import get_environment, Environment
from .base import ENV

environment = get_environment(ENV)
if environment == Environment.PRODUCTION.value:
    from .prod import *
elif environment == Environment.TEST.value:
    from .test import *
else:
    from .development import *
