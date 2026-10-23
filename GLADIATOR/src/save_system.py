# ============================================================
#  GLADIATOR ARENA - Save System
# ============================================================
import json, os, time
from settings import SAVE_PATH


class SaveSystem:
    @staticmethod
    def save(player, settings_data=None):
        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
        data = {
            'timestamp': time.time(),
            'version':   '1.0',
            'player':    player.to_dict(),
            'settings':  settings_data or {},
        }
        with open(SAVE_PATH, 'w') as f:
            json.dump(data, f, indent=2)
        return True

    @staticmethod
    def load():
        if not os.path.exists(SAVE_PATH):
            return None
        try:
            with open(SAVE_PATH, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f'[SaveSystem] Load error: {e}')
            return None

    @staticmethod
    def has_save():
        return os.path.exists(SAVE_PATH)

    @staticmethod
    def delete():
        if os.path.exists(SAVE_PATH):
            os.remove(SAVE_PATH)
