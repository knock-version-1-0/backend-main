from .base import *

DEBUG = False

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    os.environ.get('WEB_DOMAIN_ADDRESS'),
]
ALLOWED_HOSTS = ['www.knockcozynote.online', 'knockcozynote.online']
