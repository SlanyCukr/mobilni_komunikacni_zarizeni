import json
import os


class DataManager:
    def __init__(self, filename):
        self.filename = filename

    def save_data(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return {}
