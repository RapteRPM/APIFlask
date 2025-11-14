import os
from datetime import timedelta

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'SML_2025')
JWT_TOKEN_LOCATION = ["headers"]
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_HEADER_NAME = "Authorization"
JWT_HEADER_TYPE = "Bearer"
