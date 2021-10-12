import tweepy
import csv
import keyboard
from utils import *
from bs4 import BeautifulSoup


# settings
dataset_file = 'out/data_31.tsv'
proceed_existing = True
threads_per_company = 250
requests_per_company = 500
repeats = 3
company_file_path = 'companies.txt'
text_blacklist = ['\\x', '@']
negative_list = ['baal', 'balen', 'belachelijk', 'boos', 'defect', 'erbarmelijk', 'fail', 'geld terug', 'irritant',
                 'jammer', 'kortaf', 'negatief', 'niet doen', 'niet meer', 'niet waar', 'niks aan', 'nooit meer',
                 'schadelijk', 'schande', 'slecht', 'spijt', 'te duur', 'teleurstelling', 'vaag', 'verdorie', 'verpruts', 'vervelend',
                 'waardeloos', 'waardeloze']

# twitter developer API
consumer_key = 'kQWhgi3L2dKrxqS5rFB04LS2Q'
consumer_secret = 'JF4YP8j1fAwlBUnILdz4dRFWfnX4edzqGRTs05EoyjR8e1Kdjf'
access_token = '1329878486526402560-8nz9qHI46mTHOJ4iQ6Paa3QTzBYrnn'
access_token_secret = 'Tkm4qhy6op9KwdDu71RxCTuet7nTs3VmNsKCIwFONYfxF'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

conversation_lines = []

session_count = 0

force_quit = False
for x in range(repeats):
    remove_list = set()
    # fetch companies' twitter_id from text file
    companies = read_csv(company_file_path)
    # print(companies[0]['twitter_id'], companies[-1]['twitter_id'])
    company_thread_target = {}

    old_header = []
    conversations = []
    tweet_ids = set()

    # existing data
    if proceed_existing:
        old_data, old_company_info, next_id, old_conversation_ids, old_header = read_thread_dataset(dataset_file)
        old_conversations = old_data
        print(old_company_info)

        old_csv = read_csv(dataset_file, encoding='UTF-8', has_header=True, keep_header=False, lists=True)
        new_csv_1 = []
        conversation_ids = old_conversation_ids
        for company in companies:
            company_id = company['twitter_id']
            if company_id in old_company_info:
                has = old_company_info[company_id]
                needs = threads_per_company
                left = needs - has
            else:
                left = threads_per_company
            if left > 0:
                company_thread_target[company_id] = left
    else:
        next_id = 1
        conversation_ids = set()
        for company in companies:
            company_id = company['twitter_id']
            company_thread_target[company_id] = threads_per_company
    if len(company_thread_target) == 0:
        print('dataset complete!')
        exit()

    # ID, Thread_id, Company, Goederen_of_dienst, Score_sentimentanalyse, Datetime, Text, Likes, Retweets
    tweets = []
    # ID, Thread_id, Company, Goederen_of_dienst, Score_sentimentanalyse, Datetime, Total_likes, Total_retweets,
    # [text,likes,retweets,text,likes,retweets...]

    longest_thread = 0

    print('companies remaining: ' + str(len(company_thread_target)))

    for company in companies:
        if force_quit:
            break
        company_id = company['twitter_id']

        if company_id not in company_thread_target:
            print('no threads required for ' + company_id)
            continue

        # print('company: ' + company_id)
        company_type = company['type']

        skip_counter = 0
        comp_threads = threads_per_company - company_thread_target[company_id]
        current_request = 0
        # for tweet in tweepy.Cursor(api.search, q="to:{} -filter:retweets".format(company_id),
        #                            lang="nl",
        #                            since="2015-01-01", tweet_mode='extended').items(requests_per_company):
        for tweet in api.user_timeline(company_id, count=requests_per_company, tweet_mode="extended", lang='nl'):

            if keyboard.is_pressed("x"):
                force_quit = True
                break

            if skip_counter >= 30:
                pass

            skip_counter += 1
            current_request += 1
            print(company_id + ' ' + str(current_request) + '/' + str(requests_per_company))
            # initialise tweet parameters
            tweet_dict = {}
            ID = tweet.id_str
            Thread_id = 'None'
            Company = company_id
            Goederen_of_dienst = company_type
            Datetime = tweet.created_at
            Text = tweet.full_text
            if hasattr(tweet, 'favorite_count'):
                Likes = str(tweet.favorite_count)
                # print(Likes)
            else:
                Likes = '0'
            if hasattr(tweet, 'retweet_count'):
                Retweets = str(tweet.retweet_count)
            else:
                Retweets = '0'
            In_reply_to = tweet_is_reply_to(tweet)
            clean_tweet_text = clean_text(Text, blacklist=text_blacklist)  # clean text
            Score_sentimentanalyse = str(text_get_sentiment(clean_tweet_text))  # sentiment analysis

            # check duplicate
            if ID in tweet_ids:
                continue
            else:
                tweet_ids.add(ID)

            # set tweet dict fields (thread_id still needs to be determined)
            tweet_dict['ID'] = ID
            tweet_dict['Thread_id'] = Thread_id
            tweet_dict['Company'] = Company
            tweet_dict['Goederen_of_dienst'] = Goederen_of_dienst
            tweet_dict['Score_sentimentanalyse'] = Score_sentimentanalyse
            tweet_dict['Datetime'] = Datetime
            tweet_dict['Text'] = Text
            tweet_dict['Likes'] = Likes
            tweet_dict['Retweets'] = Retweets
            tweet_dict['In_reply_to'] = In_reply_to

            conversation = {'Company': Company, 'Goederen_of_dienst': Goederen_of_dienst, 'tweets': []}

            if In_reply_to == 'None':
                # for now ignore non-conversation
                continue

                # # original tweet
                # tweet_dict['Thread_id'] = ID
                # # add
                # tweets.append(tweet_dict)
                # conversation_ids.add(Thread_id)
                #
                # # ID, Thread_id, Company, Goederen_of_dienst, Score_sentimentanalyse, Datetime, Total_likes, ....
                # conversation['Thread_id'] = ID
                # conversation['Score_sentimentanalyse'] = Score_sentimentanalyse
                # conversation['Datetime'] = Datetime
                # conversation['Total_likes'] = Likes
                # conversation['Total_retweets'] = Retweets
                # conversation['tweets'].append(tweet_dict)
            else:
                # tweet is a reply
                # print(In_reply_to)
                conversation['Thread_id'] = '0'
                conversation['Score_sentimentanalyse'] = Score_sentimentanalyse
                conversation['Datetime'] = '0'
                conversation['Total_likes'] = Likes
                conversation['Total_retweets'] = Retweets
                conversation['tweets'].append([Text.replace('\n', ''), Likes, Retweets])
                target_tweet = tweet
                while True:
                    if str(target_tweet.in_reply_to_status_id) is not 'None':
                        # target tweet is a reply
                        if target_tweet.in_reply_to_status_id in tweet_ids:
                            # already registered
                            break
                        try:
                            target_tweet = api.get_status(target_tweet.in_reply_to_status_id, tweet_mode='extended')
                            tmp_fav = '0'
                            tmp_ret = '0'
                            if hasattr(target_tweet, 'favorite_count'):
                                tmp_fav = target_tweet.favorite_count
                                conversation['Total_likes'] = str(int(conversation['Total_likes']) +
                                                                  int(target_tweet.favorite_count))
                            if hasattr(target_tweet, 'retweet_count'):
                                tmp_ret = target_tweet.retweet_count
                                conversation['Total_retweets'] = str(int(conversation['Total_retweets']) +
                                                                     int(target_tweet.retweet_count))
                            conversation['tweets'].insert(0, [remove_quotes(parse_text(target_tweet.full_text.replace('\n', ''))),
                                                              tmp_fav, tmp_ret])
                            # print('succeeded! text: ' + target_tweet.full_text + ' ' + target_tweet.user.screen_name)
                        except tweepy.TweepError:
                            break

                # identify the review tweet
                review_text = conversation['tweets'][0][0]
                for tw in conversation['tweets']:
                    if company_id in tw[0]:
                        print('review tweet:')
                        print(tw[0])
                        review_text = tw[0]
                        break

                # check thread validity (more than one tweet)
                if not len(conversation['tweets']) > 1:
                    # Not a conversation: continue to next request
                    print('no conversation')
                    continue

                if detect_language(review_text) != 'nl':
                    print('not NL')
                    continue

                # check thread resolution
                if tweet_is_reply_to(target_tweet) == 'None':
                    # thread traced succesfully
                    Thread_id = target_tweet.id_str
                    conversation_ids.add(Thread_id)

                    conversation['Thread_id'] = target_tweet.id_str
                    score_sentiment = text_get_sentiment(clean_text(review_text, blacklist=text_blacklist))

                    is_negative = False
                    for negative in negative_list:
                        if negative in review_text:
                            is_negative = True

                    # is_negative = any(word in review_tweet.full_text for word in negative_list)
                    if score_sentiment < 0 or is_negative:
                        print('negative:')
                        print(review_text)
                    else:
                        print('not negative')
                        continue

                    conversation['Score_sentimentanalyse'] = str(score_sentiment)
                    conversation['Datetime'] = target_tweet.created_at
                    if len(conversation['tweets']) > longest_thread:
                        longest_thread = len(conversation['tweets'])

                else:
                    # corrupt thread: continue to next request
                    print('corrupt thread')
                    continue

                # remove old conv if is shorter
                if target_tweet.id_str in conversation_ids:
                    skiip = False
                    for curr_convs in conversations:
                        if curr_convs['Thread_id'] == target_tweet.id_str:
                            skiip = True
                            break
                    if skiip:
                        print('existing new')
                        continue

                    print('existing old')
                    while True:
                        # search old convs
                        deleted = False
                        for j, conv_line in enumerate(old_csv):
                            if conv_line[1] == target_tweet.id_str:
                                conv_tweets = chunk_list(conv_line[8:], 3)
                                old_num = len(conv_tweets)
                                new_num = len(conversation['tweets'])
                                if new_num > old_num:
                                    # mark for replace
                                    print('old:')
                                    print(conv_tweets)
                                    print('new:')
                                    print(conversation['tweets'])
                                    del old_csv[j]
                                    deleted = True
                                    break

                        # search new convs
                        # for j, conv_line in enumerate(conversations):
                        #     if conv_line['Thread_id'] == target_tweet.id_str:
                        #         conv_tweets = conv_line['tweets']
                        #         old_num = len(conv_tweets)
                        #         new_num = len(conversation['tweets'])
                        #         if new_num > old_num:
                        #             # remove dict from list
                        #             del conversations[j]
                        #             deleted = True
                        #             break
                        if not deleted:
                            break

            print('thread collected!')
            skip_counter = 0
            conversations.append(conversation)
            comp_threads += 1
            session_count += 1

            if comp_threads >= threads_per_company:
                break

    print('new threads: ' + str(len(conversations)))
    # print('tweets: ' + str(sum([len(conv['tweets']) for conv in conversations])))

    # Open/Create a file to append data
    with open(dataset_file, 'w', newline='', encoding='UTF-8') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')

        # header
        header = ['ID', 'Thread_id', 'Company', 'Goederen_of_dienst', 'Score_sentimentanalyse', 'Datetime',
                  'Total_likes', 'Total_retweets']
        for thread_tweet in range(longest_thread):
            header.append('Text_tweet_' + str(thread_tweet + 1))
            header.append('Likes_tweet_' + str(thread_tweet + 1))
            header.append('Retweets_tweet_' + str(thread_tweet + 1))
        if proceed_existing:
            if len(header) < len(old_header):
                header = old_header
        writer.writerow(header)

        counter = 0
        update_counter = 0
        if proceed_existing:
            for old_conv in old_csv:
                if old_conv[1] not in remove_list:
                    counter += 1
                    conv_row = [str(counter)]
                    conv_row.extend(old_conv[1:])
                    writer.writerow(conv_row)
                else:
                    print('updated thread')
                    update_counter += 1

        for conv in conversations:
            counter += 1
            row = [str(counter), conv['Thread_id'], conv['Company'], conv['Goederen_of_dienst'],
                   conv['Score_sentimentanalyse'], conv['Datetime'], conv['Total_likes'], conv['Total_retweets']]
            row_ext_tweets = [item for sublist in conv['tweets'] for item in sublist]
            row.extend(row_ext_tweets)
            writer.writerow(row)
    proceed_existing = True
    if force_quit:
        print('forced exit.')
        print('session count: ', session_count)
        exit()

    # for tweet_dict in tweets:
    #     row = [tweet_dict['ID'], tweet_dict['Thread_id'], tweet_dict['Company'], tweet_dict['Goederen_of_dienst'],
    #            tweet_dict['Score_sentimentanalyse'], tweet_dict['Datetime'], tweet_dict['Text'].replace('\n', ''),
    #            tweet_dict['Likes'], tweet_dict['Retweets'], tweet_dict['In_reply_to']]
    #     writer.writerow(row)
print('session count: ', session_count)
if proceed_existing:
    print('update counter: ', update_counter)
