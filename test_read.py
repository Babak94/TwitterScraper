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


tsv_file = 'out/data_31_merged.tsv'
data, company_dict, next_id, conversation_ids, data[0] = read_thread_dataset(tsv_file)
total = sum(company_dict.values())
companies = company_dict.keys()
print(company_dict)
print(sum(company_dict.values()))

# GET CSV DATA
lines = read_csv(tsv_file, encoding='UTF-8', keep_header=True, lists=True)
#print(len(lines))
#print(lines[-1])

# def header
header = lines[0].copy()
del lines[0]
##########################


# # MERGE tweet parts
# uncounted_threads = []
# num_postnl = 0
# counter = 0
# for i, line in enumerate(lines):
#     base_line = line[:8]
#     tweets = chunk_list(line[8:], 3)
#     new_tweets = []
#     for tw in tweets:
#         tw = list(tw)
#         txt = tw[0]
#         last_word = txt.split()[-1]
#         one_before_last = txt.split()[len(txt.split())-2]
#         try:
#             two_before_last = txt.split()[len(txt.split())-3]
#         except:
#             two_before_last = one_before_last
#         first_word = txt.split()[0]
#         added = False
#         if ('2/2' in last_word) or ('2/2' in one_before_last) or ('2/2' in two_before_last):
#             # append it to 1/2 in new_tweets
#             for m, nt in enumerate(new_tweets):
#                 if '1/2' in nt[0]:
#                     new_tweets[m][0] = new_tweets[m][0] + ' ' + txt
#                     new_tweets[m][1] = str(int(new_tweets[m][1]) + int(tw[1]))
#                     new_tweets[m][2] = str(int(new_tweets[m][2]) + int(tw[2]))
#                     # print(new_tweets[m])
#                     counter += 1
#                     added = True
#                     break
#         elif ('2/3' in last_word) or ('2/3' in one_before_last) or ('2/3' in two_before_last):
#             # append it to 1/2 in new_tweets
#             for m, nt in enumerate(new_tweets):
#                 if '1/3' in nt[0]:
#                     new_tweets[m][0] = new_tweets[m][0] + ' ' + txt
#                     new_tweets[m][1] = str(int(new_tweets[m][1]) + int(tw[1]))
#                     new_tweets[m][2] = str(int(new_tweets[m][2]) + int(tw[2]))
#                     # print(new_tweets[m])
#                     counter += 1
#                     added = True
#                     break
#         elif ('3/3' in last_word) or ('3/3' in one_before_last) or ('3/3' in two_before_last):
#             # append it to 1/2 in new_tweets
#             for m, nt in enumerate(new_tweets):
#                 if '2/3' in nt[0]:
#                     new_tweets[m][0] = new_tweets[m][0] + ' ' + txt
#                     new_tweets[m][1] = str(int(new_tweets[m][1]) + int(tw[1]))
#                     new_tweets[m][2] = str(int(new_tweets[m][2]) + int(tw[2]))
#                     # print(new_tweets[m])
#                     counter += 1
#                     added = True
#                     break
#         elif ('2/4' in last_word) or ('2/4' in one_before_last) or ('2/4' in two_before_last):
#             # append it to 1/2 in new_tweets
#             for m, nt in enumerate(new_tweets):
#                 if '1/4' in nt[0]:
#                     new_tweets[m][0] = new_tweets[m][0] + ' ' + txt
#                     new_tweets[m][1] = str(int(new_tweets[m][1]) + int(tw[1]))
#                     new_tweets[m][2] = str(int(new_tweets[m][2]) + int(tw[2]))
#                     # print(new_tweets[m])
#                     counter += 1
#                     added = True
#                     break
#         elif ('3/4' in last_word) or ('3/4' in one_before_last) or ('3/4' in two_before_last):
#             # append it to 1/2 in new_tweets
#             for m, nt in enumerate(new_tweets):
#                 if '2/4' in nt[0]:
#                     new_tweets[m][0] = new_tweets[m][0] + ' ' + txt
#                     new_tweets[m][1] = str(int(new_tweets[m][1]) + int(tw[1]))
#                     new_tweets[m][2] = str(int(new_tweets[m][2]) + int(tw[2]))
#                     # print(new_tweets[m])
#                     counter += 1
#                     added = True
#                     break
#         elif ('4/4' in last_word) or ('4/4' in one_before_last) or ('4/4' in two_before_last):
#             # append it to 1/2 in new_tweets
#             for m, nt in enumerate(new_tweets):
#                 if '3/4' in nt[0]:
#                     new_tweets[m][0] = new_tweets[m][0] + ' ' + txt
#                     new_tweets[m][1] = str(int(new_tweets[m][1]) + int(tw[1]))
#                     new_tweets[m][2] = str(int(new_tweets[m][2]) + int(tw[2]))
#                     # print(new_tweets[m])
#                     counter += 1
#                     added = True
#                     break
#         else:
#             new_tweets.append(tw)
#             added = True
#
#         if not added:
#             new_tweets.append(tw)
#
#     # extend new conv with whatever is in new_tweets
#     for twt in new_tweets:
#         base_line.extend(twt)
#     uncounted_threads.append(base_line[1:])
# for tr in uncounted_threads:
#     print(tr)
# print(counter)
# print(len(uncounted_threads))
##############################


# TEST
# uncounted_threads = []
# for i, line in enumerate(lines):
#     tweets = chunk_list(line[8:], 3)
#     if len(tweets) < 2:
#         print(tweets)


# REMOVE EXTRA FIELDS IN FRONT
# uncounted_threads = []
# for i, line in enumerate(lines):
#     trim_fields = 0
#     for field in line:
#         if len(field) < 6:
#             trim_fields += 1
#         else:
#             #print(field)
#             break
#     uncounted_threads.append(line[trim_fields:])
##############################

# # DUPLICATE THREAD HANDLING
# uncounted_threads = []
# duplicates = set()
# ids = set()
# dupes = 0
# for i, line in enumerate(lines):
#     current_id = line[1]
#     if current_id in ids:
#         dupes += 1
#         duplicates.add(current_id)
#     else:
#         ids.add(current_id)
# print(dupes)
#
# # append with already-uniques
# for i, line in enumerate(lines):
#     current_id = line[1]
#     if current_id not in duplicates:
#         uncounted_threads.append(line[1:])
#
# # append with longest from duplicates
# for dupe in duplicates:
#     longest = []
#     dupe_count = 0
#     for i, line in enumerate(lines):
#         current_id = line[1]
#         if dupe == current_id:
#             dupe_count += 1
#             tweets = chunk_list(line[8:], 3)
#             # print(tweets)
#             len_curr = len(tweets)
#             old_tweets = chunk_list(longest[8:], 3)
#             len_old = len(old_tweets)
#             if len_curr > len_old:
#                 #print('old:', len_old, ' new:', len_curr)
#                 longest = line
#     # print(dupe_count)
#     # print(longest)
#
#     if len(longest) > 0:
#         uncounted_threads.append(longest[1:])
#     # print('__________________________________________________________')
#######################################################

# # keep dutch tweets only
# count = 0
# new_lines = []
# for i, line in enumerate(lines):
#     company = line[2]
#     line_tweets = chunk_list(line[8:], 3)
#     conversation = [ln[0] for ln in line_tweets]
#     review_tweet = conversation[0]
#     for tweet in conversation:
#
#         # determination of the review tweet
#         if company in tweet:
#             review_tweet = tweet
#             break
#
#     lang = detect_language(review_tweet)
#     # print(lang)
#     if lang == 'nl':
#         new_score = text_get_sentiment(clean_text(review_tweet, blacklist=[]))
#
#         # test negativity
#         is_negative = False
#         for negative in negative_list:
#             if negative in review_tweet:
#                 is_negative = True
#
#         if is_negative or new_score < 0:
#             count += 1
#             new_line = [str(count)]
#             new_line.extend(line[1:4])
#             new_line.extend([str(new_score)])
#             new_line.extend(line[5:])
#             new_lines.append(new_line)
#
#print(len(new_lines))
#print(new_lines[-1])
#print('new thread count: ', count)

# CLEAN QUOTE CHAINS
# new_lines_2 = []
# for line2 in lines:
#     new_line_2 = []
#     for field in line2:
#         new_field = field
#         changed = False
#         if '\"\"' in field:
#             print(field)
#             changed = True
#             new_words = []
#             words = field.split()
#             for w in words:
#                 new_w = w
#                 if '\"\"' in w:
#                     new_w = w.replace('\"', '')
#                     # print('words: ', words)
#                 new_words.append(new_w)
#
#             new_field = ' '.join(new_words)
#         if changed:
#             print(new_field)
#         new_line_2.append(new_field)
#     new_lines_2.append(new_line_2)
##########################

# # WRITE UNCOUNTED AS COUNTED
# with open('out/data_31_merged.tsv', 'w', newline='', encoding='UTF-8') as tsvfile:
#     writer = csv.writer(tsvfile, delimiter='\t')
#     writer.writerow(header)
#     new_counter = 0
#     for u in uncounted_threads:
#         new_counter += 1
#         new_thread = [str(new_counter)]
#         new_thread.extend(u)
#         writer.writerow(new_thread)
#
# print(new_counter)


# # WRITE
# thread_list = new_lines_2
# with open('out/data_31_unquoted.tsv', 'w', newline='', encoding='UTF-8') as tsvfile:
#     writer = csv.writer(tsvfile, delimiter='\t')
#     writer.writerow(header)
#     for u in thread_list:
#         writer.writerow(u)
