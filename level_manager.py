import json
from settings import LEVELS_PATH


class LevelManager:

    def __init__(self):
        self.current_level = 1

    def load_level(self, level_number):
        path = f"{LEVELS_PATH}level_{level_number:02}.json"

        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def next_level(self):
        self.current_level += 1
