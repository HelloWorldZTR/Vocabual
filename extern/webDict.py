import requests

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
    except:
        pic = None
    return (expl, phrs_list, pic)

def query_spelling(word) -> str:
    url = f"http://dict.youdao.com/dictvoice?type=0&audio={word}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.content
    else:
        return None

# print(query_youdao("abandon"))  # ['放弃；遗弃；离弃']
