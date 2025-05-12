from hashlib import sha256
from functions import load_json, save_json
import os

users_json_path = 'usuarios.json'

def define_json_path(dir_json: str) -> str:
    global users_json_path
    users_json_path = os.path.join(dir_json, users_json_path)

def load_users():
    try:
        return load_json(users_json_path)
    except FileNotFoundError:
        return {}

def verify_user(username, password, users):
    user = users.get(username)
    if user and user['password'] == sha256(password.encode()).hexdigest():
        return True
    return False

def register_user(username, password, users):
    if username in users:
        return False
    users[username] = {
        'password': sha256(password.encode()).hexdigest(),
        'saved_journals': []
    }
    save_json(users, users_json_path)
    return True

def save_journal_for_user(username, journal_id, users):
    users = load_users()
    if username in users:
        if journal_id not in users[username]['saved_journals']:
            users[username]['saved_journals'].append(journal_id)
            save_json(users, users_json_path)

def get_saved_journals(username, users):
    users = load_users()
    return users.get(username, {}).get('saved_journals', [])

def delete_saved_journal(username, journal_id):
    users = load_users()
    if username in users and journal_id in users[username]['saved_journals']:
        users[username]['saved_journals'].remove(journal_id)
        save_json(users, users_json_path)
        return True
    return False
