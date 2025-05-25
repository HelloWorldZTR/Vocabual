import os
import json

path = "settings.json"
path = os.path.join(os.path.dirname(__file__), path)

class Settings:
    def __init__(self):
        if os.path.exists(path):
            self.settings = {}
            self.load_settings()
        else :
            self.load_default_settings()
            self.save_settings()
    def load_default_settings(self):
        self.book_id = None
        self.word_cnt = 0
        self.daily_word_cnt = 30
        self.learned = []
    def load_settings(self):
        with open(path, "r", encoding="utf-8") as f:
            self.settings = json.load(f)
        self.book_id = self.settings.get("book_id", None)
        self.word_cnt = self.settings.get("word_cnt", 0)
        self.daily_word_cnt = self.settings.get("daily_word_cnt", 30)
        self.learned = self.settings.get("learned", [])
    def save_settings(self):
        self.settings = {
            "book_id": self.book_id,
            "word_cnt": self.word_cnt,
            "daily_word_cnt": self.daily_word_cnt,
            "learned": self.learned
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=4)