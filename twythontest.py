# from twython import Twython
#
# twitter = Twython('kQWhgi3L2dKrxqS5rFB04LS2Q', 'JF4YP8j1fAwlBUnILdz4dRFWfnX4edzqGRTs05EoyjR8e1Kdjf',
#                   '1329878486526402560-8nz9qHI46mTHOJ4iQ6Paa3QTzBYrnn', 'Tkm4qhy6op9KwdDu71RxCTuet7nTs3VmNsKCIwFONYfxF')
#
# results = twitter.cursor(twitter.search, q='to:bol_com -filter:retweets', tweet_mode='extended', lang='nl', count=30)
# for result in results:
#     print(result['id_str'])

from utils import *
import csv


# x = [1,2,3,4]
# for i in reversed(range(len(x))):
#      print(i)


# text = "\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"hoi @bol_com dit is niet oke! \"\"\"\""
# print(text)
# print(remove_quotes(parse_text(text.replace('\n', ''))))


# negative_list = ['baal', 'balen', 'belachelijk', 'boos', 'defect', 'erbarmelijk', 'fail', 'geld terug', 'irritant',
#                  'jammer', 'kortaf', 'negatief', 'niet doen', 'niet meer', 'niet waar', 'niks aan', 'nooit meer',
#                  'schadelijk', 'schande', 'slecht', 'spijt', 'te duur', 'teleurstelling', 'vaag', 'verdorie', 'verpruts', 'vervelend',
#                  'waardeloos', 'waardeloze']


tsv_file = 'out/data_nl_neg.tsv'
data, company_dict, next_id, conversation_ids, data[0] = read_thread_dataset(tsv_file)
total = sum(company_dict.values())
companies = company_dict.keys()
print(company_dict)
print(sum(company_dict.values()))