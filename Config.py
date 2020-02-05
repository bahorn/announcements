import os

from dotenv import load_dotenv
load_dotenv()

# All possible config options
config_options = [
    'PUSHER_APP_ID',
    'PUSHER_KEY',
    'PUSHER_SECRET',
    'PUSHER_CLUSTER',
    'PUSHER_CHANNEL',
    'SHEET',
    'SHEET_RANGE'
]


class Settings:
    pass

for key in config_options:
    setattr(Settings, key, os.getenv(key))
