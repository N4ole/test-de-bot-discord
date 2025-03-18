import json
import os
from dotenv import load_dotenv

# 🔐 Charger .env
load_dotenv()

# ✅ Token sécurisé
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# 📂 Fichier de config dynamique
CONFIG_FILE = 'config_data.json'

# Charger ou créer config JSON
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({}, f)

with open(CONFIG_FILE, 'r') as f:
    config_data = json.load(f)

# 🔧 Channel global logs via .env
LOG_CHANNEL_ID = int(os.getenv('LOGS_SENT_CHANNEL_ID', 0))

# 🕵️‍♂️ Watchlist utilisateurs
WATCHED_USERS = config_data.get('watched_users', [])


def add_to_watchlist(user_id):
    if user_id not in WATCHED_USERS:
        WATCHED_USERS.append(user_id)
        config_data['watched_users'] = WATCHED_USERS
        save_config()


def remove_from_watchlist(user_id):
    if user_id in WATCHED_USERS:
        WATCHED_USERS.remove(user_id)
        config_data['watched_users'] = WATCHED_USERS
        save_config()


def is_watched(user_id):
    return user_id in WATCHED_USERS

# 🔗 Salons logs individuels (user)


def save_user_log_channel(user_id, channel_id):
    config_data.setdefault('watchlist_channels', {})[str(user_id)] = channel_id
    save_config()


def get_user_log_channel(user_id):
    return config_data.get('watchlist_channels', {}).get(str(user_id))

# 🗂️ Salons logs par type : message, edit, delete, voice


def save_log_channel(log_type, channel_id):
    config_data.setdefault('log_channels', {})[log_type] = channel_id
    save_config()


def get_log_channel(log_type):
    return config_data.get('log_channels', {}).get(log_type)

# 💾 Sauvegarde config JSON


def save_config():
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=4)
