import requests


def translate_article(article):
    query_params = {'key': 'trnsl.1.1.20160222T224653Z.00721123b6197657.e894adadf82349bb5d89d907b7de173b017779e0',
                    'text': article,
                    'lang': 'en'}

    r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=query_params)
    if r.status_code == requests.codes.ok:
        yandex_status_code = int(r.text[8:11])
        if yandex_status_code == 200:
            text = r.json()['text'][0]
            return text
        # TODO: another error codes https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/
        # if create new apikey or something else
        else:
            # TODO: add to log!
            # TODO: count chars?
            pass
    else:
        return None
