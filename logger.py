import json
import os

class Logger:
    def __init__(self, log_path):
        self.log_path = log_path
        if not os.path.exists(log_path):
            os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def log(self, command):
        log_entry = {"command": command}
        with open(self.log_path, "a") as log_file:
            json.dump(log_entry, log_file)
            log_file.write("\n")
