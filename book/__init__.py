import pandas as pd
import os
from word import Word
from book import Book

def get_root_dir():
    """获取项目根目录"""
    return os.path.dirname(os.path.abspath(__file__))

def load_data_files():
    """加载所有数据文件"""
    data_dir = os.path.join(get_root_dir(), 'DictionaryData')
    files = {
        'word': pd.read_csv(os.path.join(data_dir, 'word.csv'), sep=">"),
        'translation': pd.read_csv(os.path.join(data_dir, 'word_translation.csv')),
        'book': pd.read_csv(os.path.join(data_dir, 'book.csv'), sep=">"),
        'relation': pd.read_csv(os.path.join(data_dir, 'relation_book_word.csv'), sep=">")
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
            word = word_dict[word_id]
            
            # 双向添加关系（不存储关系ID）
            book.word_list.append(word)
            word.book_list.append(book)

def init_system():
    """
    初始化系统
    返回:
        tuple: (word_dict, book_dict)
    """
    #print("正在初始化数据系统...")
    try:
        data = load_data_files()
        word_dict = create_word_objects(data['word'], data['translation'])
        book_dict = create_book_objects(data['book'])
        build_relationships(data['relation'], word_dict, book_dict)
        
        #print(f"加载完成: {len(word_dict)} 单词, {len(book_dict)} 书籍")
        return word_dict, book_dict
        
    except Exception as e:
        #print(f"初始化失败: {str(e)}")
        return {}, {}

words, books = init_system()