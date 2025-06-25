import urllib.request
import requests
import tempfile
import urllib

"""
Functions to query web dictionaries.
"""
def query_youdao(word) -> list:
    url = f"https://dict.youdao.com/jsonapi?q={word}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    data = res.json()
    try:
        expl = data['ec']['word'][0]['trs']
        expl =  [tr['tr'][0]['l']['i'] for tr in expl]
    except:
        expl = None
    try:
        phrs = data['phrs']['phrs']
        phrs_list = []
        for phr in phrs:
            hd = phr['phr']['headword']['l']['i']
            trs = phr['phr']['trs'][0]['tr']['l']['i']
            phrs_list.append((hd, trs))
    except Exception as e:
        print(f"Error parsing phrases: {e}")
        phrs_list = None
    try:
        pic = data['pic_dict']['pic'][0]['image']
        temp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        with open(temp.name, 'wb') as f:
            f.write(requests.get(pic).content)
        pic = temp.name
    except:
        pic = None
    return (expl, phrs_list, pic)

def query_spelling(word:str, type:int=0) -> tempfile.NamedTemporaryFile:
    """
    查询单词的发音
    type: 0 - 英式发音, 1 - 美式发音
    """
    url = f"http://dict.youdao.com/dictvoice?type={type}&audio={word}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    try:
        urllib.request.urlretrieve(url, temp.name)
        return temp.name
    except Exception as e:
        print(f"[Error] An error occurred while fetching audio for {word}: {e}")
    
# print(query_spelling("abandon", 0))  # 英式发音
# print(query_spelling("abandon", 1))  # 美式发音
# print(query_youdao("abandon"))  # ['放弃；遗弃；离弃']
