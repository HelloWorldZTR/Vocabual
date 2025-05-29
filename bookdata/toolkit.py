import os
import pandas as pd

def to_feather():
    paths = [
        'book.csv',
        'word.csv',
        # 'word_translation.csv',
        'relation_book_word.csv'
    ]
    data_dir = os.path.join(os.path.dirname(__file__), 'DictionaryData')
    for path in paths:
        csv_path = os.path.join(data_dir, path)
        feather_path = os.path.join(data_dir, path.replace('.csv', '.feather'))
        df = pd.read_csv(csv_path, sep='>')
        df.to_feather(feather_path)
        print(f"Converted {path} to {feather_path}")
    print("All files converted to Feather format.")

# to_feather()

def to_feather2():
    path = os.path.join(os.path.dirname(__file__), 'DictionaryData', 'word_translation.csv')  
    df = pd.read_csv(path)
    df.to_feather(path.replace('.csv', '.feather'))
    print(f"Converted word_translation.csv to Feather format at {path.replace('.csv', '.feather')}")

# to_feather2()
from openai import OpenAI

def translate_untranslated():
    API_KEY = '' # : Replace with your own Deepseek API key
    model_name = "deepseek-chat"
    client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
    prompt = """将下面的单词或短语翻译成中文，每行一条
如果是单词，输出词性缩写+翻译
如果有多个含义，输出词性缩写+翻译1，词性缩写+翻译2
不要输出任何其他内容，只输出翻译结果，一行一条
"""
    
    words = pd.read_feather(os.path.join(os.path.dirname(__file__), 'word.feather'))
    wordlist = []
    for i, row in words.iterrows():
        if row['translation'] == '暂无翻译' or row['translation'] == '':
            wordlist.append((i, row['word']))
    print(f"Total words to translate: {len(wordlist)}")
    batch_size = 20
    for i in range(0, len(wordlist), batch_size):
        if i + batch_size > len(wordlist):
            batch_size = len(wordlist) - i # Adjust batch size for the last batch
        batch = wordlist[i:i + batch_size]
        batch_words = [word[1] for word in batch]
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "\n".join(batch_words)}
                ],
                stream=False,
                temperature=0.2,
                max_tokens=1000
            )
            translations = response.choices[0].message.content.strip().split('\n')
            for j, translation in enumerate(translations):
                index = batch[j][0]
                words.at[index, 'translation'] = translation
        except Exception as e:
            print(f"Error occurred while translating batch: {e}")
        finally:
            words.to_feather(os.path.join(os.path.dirname(__file__), 'word2.feather'))
            print(f"Batch {i // batch_size + 1} translated and saved.")

# translate_untranslated()

def remove_word_from_translation():
    word_df = pd.read_feather(os.path.join(os.path.dirname(__file__), 'word.feather'))
    for i, row in word_df.iterrows():
        word = str(row['word'])
        translation = str(row['translation'])
        if word in translation:
            translation = translation.replace(word, '').strip()
        # Remove dashes
        translation = translation.strip('-:').strip()
        if '名词' in translation and 'n.' not in translation:
            translation = translation.replace('名词', 'n.')
        elif '动词' in translation and 'v.' not in translation:
            translation = translation.replace('动词', 'v.')
        elif '形容词' in translation and 'adj.' not in translation:
            translation = translation.replace('形容词', 'adj.')
        elif '副词' in translation and 'adv.' not in translation:
            translation = translation.replace('副词', 'adv.')
        word_df.at[i, 'translation'] = translation
    word_df.to_feather(os.path.join(os.path.dirname(__file__), 'word.feather'))

remove_word_from_translation()

def print_word_translation():
    word_df = pd.read_feather(os.path.join(os.path.dirname(__file__), 'word.feather'))
    for i, row in word_df.iterrows():
        print(f"{row['word']}: {row['translation']}")
        if i> 100:
            break
print_word_translation()