from decouple import config
from fastapi.middleware.cors import CORSMiddleware

# DESCRIPTION
API_METADATA = {
    'title': 'Youtube Comments',
    'description': 'Put an url to return the comments in the specified formats',
    'version': '0.0.1',
    'docs_url': '/'  # Documentation (http://localhost:8000/)
}

# SECURITY WARNING: keep the secret key used in production secret!
# TO GET A KEY STRING RUN: [openssl rand -hex 42] OR [openssl rand -base64 42]
SECRET_KEY_YOUTUBE = config('SECRET_KEY_YOUTUBE')

ALLOWED_HOSTS = ['http://localhost:3000']

# Cross-Origin Resource Sharing
MIDDLEWARE = {
    'middleware_class': CORSMiddleware,
    'allow_origins': ALLOWED_HOSTS or ['*'],
    'allow_credentials': True,
    'allow_methods': ["*"],
    'allow_headers': ["*"],
}

# YOUTUBE API V3
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = config("SECRET_KEY_YOUTUBE")
