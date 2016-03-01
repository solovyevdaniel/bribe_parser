import re
import nltk

# Regex for place
GPE = re.compile(r'GPE.*/')

# Regex for money
re_numbers = '[0-9]+[,\.]?[0-9]*'
re_rank = 'thousand|million|billion'
re_currency = '\$|US|UAH|dollars|hryvnias|pounds|Euro'
money_pattern = r'(' + re_currency + ')?[ ]*(' + re_numbers + ')[ ]*(?=(' + re_rank + ')[ ]*(' + re_currency + ')?)|(' + re_currency + ')[ ]*(' + re_numbers + ')'
find_money_in_article = re.compile(pattern=money_pattern, flags=re.IGNORECASE)


def get_info_place(named_entities):
    places = []
    re_places = re.findall(GPE, named_entities)
    if re_places:
        for item in re_places:
            if item[4:-1] not in places:
                places.append(item[4:-1])
    return places


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


def get_info_money(article):
    money = []
    result_bribe = re.findall(find_money_in_article, article)
    if result_bribe:
        for result in result_bribe:
            currency = result[0] or result[3] or result[4]

            money_numbers = result[1] or result[5]
            money_numbers_replaced = money_numbers.replace(',', '.')

            rank_digit = rank_str_to_digit(result[2])

            total_sum_of_bribe = money_numbers_replaced * rank_digit
            money.append((total_sum_of_bribe, currency))
    return money


def article_processing(article):
    named_entities = None
    try:
        for item in article:
            tokenized = nltk.word_tokenize(item)
            tagged = nltk.pos_tag(tokenized)
            named_entities = nltk.ne_chunk(tagged)
    except:
        return None
    else:
        if named_entities:
            places = get_info_place(str(named_entities))
        else:
            places = []
        money = get_info_money(article)
    return places, money
