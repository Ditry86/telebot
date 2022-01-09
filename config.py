import os
import secrets
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    CONF_ROOT = os.path.dirname(__file__)
    SECRET_KEY = secrets.token_hex(32)
    HOST_NAME = os.environ.get('HOST_NAME')
    HOST_IP = os.environ.get('HOST_IP')
    HOST_PORT = os.environ.get('HOST_PORT')
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    HOST_URL = f"https://{HOST_NAME}/"
    CERT = os.environ.get('CERT')
    CERT_KEY = os.environ.get('CERT_KEY')


class Production(Config):
    TESTING = False
    DEBUG = False
    if not Config.HOST_NAME:
        HOST_URL = f"https://{Config.HOST_IP}/"
    DATABASE_URI = os.environ.get('CERT_KEY')


class Development(Config):
    DEBUG = True


class Testing(Config):
    TESTING = True
