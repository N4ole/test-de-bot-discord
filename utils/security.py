import json
import os
PROTECTED_OWNER_ID = 702923932239527978  # Ton ID, ne peut PAS être supprimé

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../data/owners.json")


def get_owners():
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    return data.get("owners", [])


def is_owner(user_id: int) -> bool:
    return any(owner["id"] == user_id for owner in get_owners())


def remove_owner(user_id: int) -> bool:
    if user_id == PROTECTED_OWNER_ID:
        return False  # Impossible de supprimer le grand chef
    owners = get_owners()
    updated = [o for o in owners if o["id"] != user_id]
    if len(updated) < len(owners):
        _save(updated)
        return True
    return False


def add_owner(user_id: int, name: str = "unknown", is_bot: bool = False) -> bool:
    if is_bot:
        return False  # Pas de bot dans la liste d'owners
    owners = get_owners()
    if not any(owner["id"] == user_id for owner in owners):
        owners.append({"id": user_id, "name": name})
        _save(owners)
        return True
    return False


def _save(owners):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"owners": owners}, f, indent=2)
