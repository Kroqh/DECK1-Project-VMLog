import os
from dotenv import load_dotenv
loaded = False

def get_setting(env_name):
    if not loaded:
        load_dotenv("/home/pi/Desktop/DECK1-Project-VMLog/scripts/settings.env")
        init = True
    return os.getenv(env_name)

