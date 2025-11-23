import json
import os

class OCPPReplayer:
    def __init__(self, json_path="ocpp_data.json"):
        self.json_path = json_path
        self.messages = []
        self.index = 0
        self._load()

    def _load(self):
        if not os.path.exists(self.json_path):
            print(f" OCPP JSON not found: {self.json_path}")
            return

        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                self.messages = json.load(f)

            print(f"✅ Loaded {len(self.messages)} OCPP messages.")
        except Exception as e:
            print(f" Failed to load JSON: {e}")

    def has_next(self):
        """Check if more messages exist"""
        return self.index < len(self.messages)

    def next(self):
        """Return next message, or None"""
        if not self.has_next():
            return None
        msg = self.messages[self.index]
        self.index += 1
        return msg
