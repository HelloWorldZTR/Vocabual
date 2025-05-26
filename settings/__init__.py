import os
import json
import bookdata
import datetime

path = "settings.json"
path = os.path.join(os.path.dirname(__file__), path)
settings = {}

def _load_default_settings():
    settings['book_id'] = ''
    settings['word_cnt'] = 0
    settings['daily_word_cnt'] = 30
    settings['learned'] = []
    settings['unlearned'] = []
    settings['daily_record'] = {}
    settings['daily_review_record'] = {}
    settings['favourite'] = []
    set_book_id('7f39f8317fbdb1988ef4c628') # 假设 book1 是一个有效的书籍ID
def _load_settings():
    with open(path, "r", encoding="utf-8") as f:
        settings.update(json.load(f))
    settings['book_id'] = settings.get("book_id", None)
    settings['word_cnt'] = settings.get("word_cnt", 0)
    settings['daily_word_cnt'] = settings.get("daily_word_cnt", 30)
    settings['learned'] = settings.get("learned", [])
    settings['unlearned'] = settings.get("unlearned", [])
    settings['daily_record'] = settings.get("daily_record", {})
    settings['daily_review_record'] = settings.get("daily_review_record", {})
    settings['favourite'] = settings.get("favourite", [])

def _save_settings():
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

def get_favourite_list() -> list:
    """获取收藏夹列表"""
    return [_id_to_word(word_id) for word_id in settings['favourite']]

def get_favourite_status(word_id) -> bool:
    """检查单词是否在收藏夹中"""
    assert word_id in bookdata.words, f"Word ID {word_id} does not exist in bookdata."
    return word_id in settings['favourite']

def set_book_id(book_id):
    """设置当前书籍ID"""
    settings['book_id'] = book_id
    assert book_id in bookdata.books, f"Book ID {book_id} does not exist in bookdata."
    settings['word_cnt'] = bookdata.books[book_id].word_count
    settings['learned'] = []
    settings['unlearned'] = list(bookdata.books[book_id].word_list)
    _save_settings()

def add_favourite(word_id):
    """将单词添加到收藏夹"""
    assert word_id in bookdata.words, f"Word ID {word_id} does not exist in bookdata."
    if word_id not in settings['favourite']:
        settings['favourite'].append(word_id)
        _save_settings()

def remove_favourite(word_id):
    """从收藏夹中移除单词"""
    assert word_id in bookdata.words, f"Word ID {word_id} does not exist in bookdata."
    if word_id in settings['favourite']:
        settings['favourite'].remove(word_id)
        _save_settings()

def _id_to_word(word_id):
    """将单词ID转换为单词对象"""
    if word_id in bookdata.words:
        return bookdata.words[word_id]
    else:
        raise ValueError(f"Word ID {word_id} does not exist in bookdata.")

def get_todays_word_list()-> list:
    """获取今天的单词列表,list[Word]"""
    if settings['book_id'] is None:
        return []
    book = bookdata.books[settings['book_id']]
    if len(settings['unlearned']) < settings['daily_word_cnt']:
        return [_id_to_word(word_id) for word_id in settings['unlearned']]
    else:
        return [_id_to_word(word_id) for word_id in settings['unlearned'][:settings['daily_word_cnt']]]

def set_learned(word_id):
    """将单词设置为已学(注意，如果错了也是已学习！)"""
    if word_id in settings['unlearned']:
        settings['unlearned'].remove(word_id)
    if word_id not in settings['learned']:
        settings['learned'].append(word_id)
    
    today = datetime.date.today().isoformat()
    if today not in settings['daily_record']:
        settings['daily_record'][today] = []
    settings['daily_record'][today].append(word_id)
    _save_settings()

def set_reviewed(word_id):
    """将单词设置为已复习,只有对了才算复习过"""
    if word_id in settings['favourite']:
        settings['favourite'].remove(word_id)
    today = datetime.date.today().isoformat()
    if today not in settings['daily_review_record']:
        settings['daily_review_record'][today] = []
    settings['daily_review_record'][today].append(word_id)
    _save_settings()

if os.path.exists(path):
    settings = {}
    _load_settings()
else :
    _load_default_settings()
    _save_settings()
