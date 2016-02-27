import re
import nltk
from . import translate_article as ta

# Regex for place
GPE = re.compile(r'GPE.*/')

# Regex for money
re_numbers = '[0-9]+[,\.]?[0-9]*'
re_rank = 'thousand|million|billion'
re_currency = '\$|US|UAH|dollars|hryvnias|pounds|Euro'
money_pattern = r'(' + re_currency + ')?[ ]*(' + re_numbers + ')[ ]*(?=(' + re_rank + ')[ ]*(' + re_currency + ')?)|(' + re_currency + ')[ ]*(' + re_numbers + ')'
find_money_in_article = re.compile(pattern=money_pattern, flags=re.IGNORECASE)


def get_info_place(named_entities):
    place = []
    # todo rename answer
    answer = re.findall(GPE, str(named_entities))
    if answer:
        for item in answer:
            if item[4:-1] not in place:
                place.append(item[4:-1])
    else:
        return None
    return place


def rank_str_to_digit(rank):
    ranks = {
        'thousand': 1000,
        'million': 1000000,
        'billion': 1000000000
    }
    if rank in ranks.keys():
        digit_rank = ranks[rank]
        return digit_rank
    else:
        return 1

# Todo
def get_info_money(article):
    money = []
    result_bribe = re.findall(find_money_in_article, article)
    if result_bribe:
        for result in result_bribe:
            if result[0] or result[3] or result[4]:
                currency = result[0] or result[3] or result[4]
            if result[1] or result[5]:
                money_numbers = result[1] or result[5]
                money_numbers_replaced = money_numbers.replace(',', '.')
            if result[2]:
                rank_digit = rank_str_to_digit(result[2])

            total_sum_of_bribe = money_numbers_replaced * rank_digit

#Todo
def article_processing(article):
    try:
        for item in article:
            tokenized = nltk.word_tokenize(item)
            tagged = nltk.pos_tag(tokenized)
            named_entities = nltk.ne_chunk(tagged)

            get_info_place(named_entities)
            get_info_money(article)
    except Exception:
        return 'azazaaza lalka'
