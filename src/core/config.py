import os
import dotenv


dotenv.load_dotenv()

# LOGGING
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO')

# DB
DATABASE_URI = os.environ.get('DATABASE_URI', 'mongodb://root:root@localhost:27017/')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'openagridb')
OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY', '')

# ALLOWED_HOSTS
EXTRA_ALLOWED_HOSTS = os.environ.get('EXTRA_ALLOWED_HOSTS', "*").replace(' ', '').split(',')

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', ''))
KEY = os.environ.get('JWT_KEY', '')
ALGORITHM = os.environ.get('ALGORITHM', '')
CRYPT_CONTEXT_SCHEME = os.environ.get('CRYPT_CONTEXT_SCHEME', '')
