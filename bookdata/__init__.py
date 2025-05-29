import pandas as pd
import os
import time
import json

class Word:
    def __init__(self, id, word, phonetic_uk, phonetic_us,difficulty,translation):
        self.id = id
        self.word = word
        self.phonetic_uk = phonetic_uk
        self.phonetic_us = phonetic_us
        self.difficulty = difficulty
        self.translation = translation
        # self.relation_book_word_id_list = []
        # self.book_list = []
    def __repr__(self):
        return f"Word(id={self.id}, word='{self.word}', phonetic_uk='{self.phonetic_uk}', phonetic_us='{self.phonetic_us}', difficulty={self.difficulty}, translation='{self.translation}')"
    def __str__(self):
        return self.word

class Book:
    def __init__(self, id, title, word_count, word_list=None):
        self.id = id
        self.title = title
        self.word_count = word_count
        # self.relation_book_word_id_list = []
        self.word_list = word_list if word_list is not None else []
    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}', word_count={self.word_count})"
    def __str__(self):
        return self.title


def get_root_dir():
    """获取项目根目录"""
    return os.path.dirname(os.path.abspath(__file__))

def load_data_files():
    """加载所有数据文件"""
    data_dir = os.path.join(get_root_dir(), 'DictionaryData')
    # files = {
    #     'word': pd.read_csv(os.path.join(data_dir, 'word.csv'), sep=">"),
    #     'translation': pd.read_csv(os.path.join(data_dir, 'word_translation.csv')),
    #     'book': pd.read_csv(os.path.join(data_dir, 'book.csv'), sep=">"),
    #     'relation': pd.read_csv(os.path.join(data_dir, 'relation_book_word.csv'), sep=">")
    # }
    files = {
        'word': pd.read_feather(os.path.join(data_dir, 'word.feather')),
        'translation': pd.read_feather(os.path.join(data_dir, 'word_translation.feather')),
        'book': pd.read_feather(os.path.join(data_dir, 'book.feather')),
        'relation': pd.read_feather(os.path.join(data_dir, 'relation_book_word.feather'))
    }
    return files

def create_word_objects(word_df, translation_df):
    """创建Word对象字典"""
    word_dict = {}
    # 合并翻译数据
    merged = pd.merge(word_df, translation_df, 
                    left_on='vc_vocabulary', 
                    right_on='word', 
                    how='left')
    
    for _, row in merged.iterrows():
        word_dict[row['vc_id']] = Word(
            id=row['vc_id'],
            word=row['vc_vocabulary'],
            phonetic_uk=row['vc_phonetic_uk'],
            phonetic_us=row['vc_phonetic_us'],
            difficulty=row['vc_difficulty'],
            translation=row['translation'] if pd.notna(row['translation']) else "暂无翻译"
        )
    return word_dict

def create_book_objects(book_df):
    """创建Book对象字典"""
    book_dict = {}
    for _, row in book_df.iterrows():
        book_dict[row['bk_id']] = Book(
            id=row['bk_id'],
            title=row['bk_name'],
            word_count=row['bk_item_num']
        )
    return book_dict

def build_relationships(relation_df, word_dict, book_dict):
    """建立书籍和单词的简单关系"""
    for _, row in relation_df.iterrows():
        book_id = row['bv_book_id']
        word_id = row['bv_voc_id']
        
        if book_id in book_dict and word_id in word_dict:
            book = book_dict[book_id]
            
            # 双向添加关系（不存储关系ID）
            book.word_list.append(word_id)
            # word.book_list.append(book)

def get_book_tree():
    json_path = os.path.join(get_root_dir(), 'book_tree.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else :
        book_df = pd.read_csv(os.path.join(get_root_dir(), 'DictionaryData', 'book.csv'), sep=">")
        book_tree = {}
        for _, row in book_df.iterrows():
            book_id = row['bk_id']
            book_title = row['bk_name']
            if row['bk_parent_id'] == '0':
                if book_id not in book_tree:
                    book_tree[book_id] = {
                        'title': book_title,
                        'children': {},
                        'id': book_id
                    }
                else:
                    # 如果书籍ID已存在，更新标题
                    book_tree[book_id]['title'] = book_title
                    book_tree[book_id]['id'] = book_id
            else:
                parent_id = row['bk_parent_id']
                if parent_id in book_tree:
                    book_tree[parent_id]['children'][book_id] = {
                        'title': book_title,
                        'children': {},
                        'id': book_id
                    }
                else:
                    # 如果父节点不存在，创建一个新的父节点
                    book_tree[parent_id] = {
                        'title': f"Unknown Parent {parent_id}",
                        'children': {
                            book_id: {
                                'title': book_title,
                                'children': {},
                                'id': book_id
                            }
                        }
                    }
        # 保存到JSON文件
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(book_tree, f, ensure_ascii=False, indent=4)
        return book_tree


def init_system():
    """
    初始化系统
    返回:
        tuple: (word_dict, book_dict)
    """
    print("[log] Loading data files...")
    st = time.time()
    try:
        data = load_data_files()
        word_dict = create_word_objects(data['word'], data['translation'])
        book_dict = create_book_objects(data['book'])
        build_relationships(data['relation'], word_dict, book_dict)
        
        #print(f"加载完成: {len(word_dict)} 单词, {len(book_dict)} 书籍")
        ed = time.time()
        print(f"[log] Data loaded successfully in {ed - st:.2f} seconds")
        return word_dict, book_dict
        
    except Exception as e:
        print(f"[err] Data load failed: {str(e)}")
        return {}, {}

# words, books = init_system()

def to_feathers():
    """将数据转换为Feather格式"""
    words, books = init_system()
    data_dir = os.path.join(get_root_dir())
    
    # 保存单词数据
    word_df = pd.DataFrame([vars(word) for word in words.values()])
    word_df.to_feather(os.path.join(data_dir, 'word.feather'))
    
    # 保存书籍数据
    book_df = pd.DataFrame([vars(book) for book in books.values()])
    book_df.to_feather(os.path.join(data_dir, 'book.feather'))
    
    print("[log] Data converted to Feather format successfully.")
    return words, books

def from_feathers():
    print("[log] Loading data from Feather format...")
    st = time.time()

    words, books = {}, {}
    data_dir = os.path.join(get_root_dir())
    word_df = pd.read_feather(os.path.join(data_dir, 'word.feather'))
    book_df = pd.read_feather(os.path.join(data_dir, 'book.feather'))

    ed1 = time.time()
    print(f"[log] time used to load data {ed1-st:.2f} seconds.")
    for _, row in word_df.iterrows():
        word = Word(
            id=row['id'],
            word=row['word'],
            phonetic_uk=row['phonetic_uk'],
            phonetic_us=row['phonetic_us'],
            difficulty=row['difficulty'],
            translation=row['translation']
        )
        words[word.id] = word
    for _, row in book_df.iterrows():
        book = Book(
            id=row['id'],
            title=row['title'],
            word_count=row['word_count'],
            word_list=row['word_list']
        )
        books[book.id] = book
    
    ed = time.time()
    print(f"[log] Data loaded from Feather format successfully in {ed - st:.2f} seconds.")
    return words, books

if os.path.exists(os.path.join(get_root_dir(), 'word.feather')) and \
   os.path.exists(os.path.join(get_root_dir(), 'book.feather')):
    words, books = from_feathers()
else:
    words, books =  to_feathers()
