import requests

key_0 = 'trnsl.1.1.20160222T224653Z.00721123b6197657.e894adadf82349bb5d89d907b7de173b017779e0'
key_1 = 'trnsl.1.1.20160309T115625Z.a26f52b59e5d19c5.3963eed3457c7fea6384406ddc8a2d9d5d62e024'
key_2 = 'trnsl.1.1.20160309T115849Z.d6de5cfc1f89b6d9.ab9dd71f8ffd88141550e682cf5c5d796faa7eb4'
key_3 = 'trnsl.1.1.20160309T120405Z.c0fbe3f7c1247a23.1727cb57d128f746c2842241ba565b639f1293cd'
key_4 = 'trnsl.1.1.20160309T120502Z.49a9a190798c493b.c03e70fd12289733cc318c4c27404875783b6da5'
keys = [key_0, key_1, key_2, key_3, key_4]


def get_yandex_status_code(status_code):
    # TODO: another error codes https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/
    if status_code == 200:
        return True
    else:
        pass


def translate_article(article):
    query_params = {'key': keys[0],
                    'text': article,
                    'lang': 'en'}

    r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=query_params)
    if r.status_code == requests.codes.ok:
        yandex_status_code = int(r.text[8:11])
        if get_yandex_status_code(yandex_status_code):
            translated_article = r.json()['text'][0]
            return translated_article
        else:
            # TODO: add to log!
            # TODO: count chars?
            pass
    else:
        return None
