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

to_feather2()