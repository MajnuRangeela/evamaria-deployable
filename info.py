import re
from os import environ
import asyncio
import json
from collections import defaultdict
from typing import Dict, List, Union
from pyrogram import Client
from logging import getLogger, info as log_info, error as log_error
from requests import get as rget
from dotenv import load_dotenv

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

class evamaria(Client):
    filterstore: Dict[str, Dict[str, str]] = defaultdict(dict)
    warndatastore: Dict[
        str, Dict[str, Union[str, int, List[str]]]
    ] = defaultdict(dict)
    warnsettingsstore: Dict[str, str] = defaultdict(dict)

    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            ":memory:",
            plugins=dict(root=f"{name}/plugins"),
            workdir=TMP_DOWNLOAD_DIRECTORY,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            parse_mode="html",
            sleep_threshold=60
        )

LOGGER = getLogger(__name__)

CONFIG_FILE_URL = environ.get('CONFIG_FILE_URL')

if CONFIG_FILE_URL:
    try:
        res = rget(CONFIG_FILE_URL)
        if res.status_code == 200:
            with open('config.env', 'wb+') as f:
                f.write(res.content)
            log_info("Succesfully got config.env from CONFIG_FILE_URL")
        else:
            log_error(f"Failed to download config.env {res.status_code}")
    except Exception as e:
        log_error(f"CONFIG_FILE_URL: {e}")

load_dotenv('config.env', override=True)
# Bot information
try:
    SESSION = environ.get('SESSION')
    API_ID = environ.get('API_ID')
    API_HASH = environ.get('API_HASH')
    BOT_TOKEN = environ.get('BOT_TOKEN')
    DATABASE_URI = environ.get('DATABASE_URI')
    DATABASE_NAME = environ.get('DATABASE_NAME')
    COLLECTION_NAME = environ.get('COLLECTION_NAME')
except:
    log_error("One or more env variables missing! Exiting now")
    exit(1)

# Bot settings

CACHE_TIME = int(environ.get('CACHE_TIME'))
if not CACHE_TIME:
    CACHE_TIME == 300
    
USE_CAPTION_FILTER = is_enabled(environ.get("USE_CAPTION_FILTER"), False)
PICS = (environ.get('PICS' ,'https://telegra.ph/file/8619a6f258621134b7576.jpg https://telegra.ph/file/d8daf35960bbb4a7f8558.jpg')).split()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []

auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(environ.get('AUTH_CHANNEL'))
USE_AS_BOT = is_enabled(environ.get('USE_AS_BOT'), False)

BASE_URL = environ.get('BASE_URL')
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

# maximum message length in Telegram
MAX_MESSAGE_LENGTH = 4096

# This is required for the plugins involving the file system.
TMP_DOWNLOAD_DIRECTORY = environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")

# the maximum number of 'selectable' messages in Telegram
TG_MAX_SELECT_LEN = environ.get("TG_MAX_SELECT_LEN", "100")

# Command
COMMAND_HAND_LER = environ.get("COMMAND_HAND_LER", "/")

#Downloader
DOWNLOAD_LOCATION = environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/AudioBoT/")

# Others
LOG_CHANNEL = int(environ.get('LOG_CHANNEL'))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT')
P_TTI_SHOW_OFF = is_enabled(environ.get('P_TTI_SHOW_OFF'), False)
IMDB = is_enabled(environ.get('IMDB'), False)
SINGLE_BUTTON = is_enabled(environ.get('SINGLE_BUTTON'), False)
CUSTOM_FILE_CAPTION = environ.get('CUSTOM_FILE_CAPTION')
BATCH_FILE_CAPTION = environ.get('BATCH_FILE_CAPTION')
IMDB_TEMPLATE = environ.get('IMDB_TEMPLATE')
LONG_IMDB_DESCRIPTION = is_enabled(environ.get('LONG_IMDB_DESCRIPTION'), False)
SPELL_CHECK_REPLY = is_enabled(environ.get('SPELL_CHECK_REPLY'), False)

try:
    FILE_STORE_CHANNEL = []
    fileChannels = environ.get('FILE_STORE_CHANNEL')
    fileChannels = fileChannels.split()
    if len(fileChannels) > 0:
        for fileChannel in fileChannels:
            FILE_STORE_CHANNEL.add(int(fileChannel))
except:
    pass

MELCOW_NEW_USERS = is_enabled(environ.get('MELCOW_NEW_USERS'), False)
PROTECT_CONTENT = is_enabled(environ.get('PROTECT_CONTENT'), False)
PUBLIC_FILE_STORE = is_enabled(environ.get('PUBLIC_FILE_STORE'), False)

MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)


LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two seperate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as diffrent buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your Currect IMDB template is {IMDB_TEMPLATE}"
