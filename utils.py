import langid
import os
import re
from nltk.tokenize import WordPunctTokenizer
from bs4 import BeautifulSoup
from pattern.text.nl import sentiment


def get_paths(input_folder):
    textfiles = []
    files = os.listdir(input_folder)
    for f in files:
        if f.endswith('.txt'):
            textfiles.append(os.path.join(input_folder, f))
    return textfiles


def tokenization(text):
    text = re.split('\W+', text)
    return text


def clean_text(text, blacklist):

    text = parse_text(text)
    text = text.strip()

    text = tweet_cleaner(text)

    words = text.split()
    keep = []
    for word in words:
        include = True
        for bad in blacklist:
            if bad in word:
                include = False
                break
        if include:
            keep.append(word)
    cleaned = ' '.join(keep)
    return cleaned


def remove_quotes(text):
    words = text.split()
    for i, word in enumerate(words):
        if '\"\"' in word:
            words[i] = word.replace('\"', '')
    new_text = ' '.join(words)
    return new_text


# def conv_get_tweetcount()

def tweet_cleaner(text):
    from bs4 import BeautifulSoup

    tok = WordPunctTokenizer()
    pat1 = r'@[A-Za-z0-9]+'
    pat2 = r'https?://[A-Za-z0-9./]+'
    #pat3 = r'#[A-Za-z0-9]+'
    combined_pat = r'|'.join((pat1, pat2))

    souped = parse_text(text)
    stripped = re.sub(combined_pat, '', souped)
    try:
        clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        clean = stripped
    letters_only = re.sub("[^a-zA-Z]", " ", clean)
    lower_case = letters_only.lower()
    # During the letters_only process two lines above, it has created unnecessay white spaces,
    # I will tokenize and join together to remove unneccessary white spaces
    words = tok.tokenize(lower_case)
    return (" ".join(words)).strip()


def parse_text(text):
    # html decode
    cleaned = BeautifulSoup(text, 'html.parser').get_text()

    return cleaned


def tweet_is_reply_to(tweet):
    if hasattr(tweet, 'in_reply_to_status_id_str'):
        is_reply_to = str(tweet.in_reply_to_status_id_str)
    else:
        is_reply_to = 'None'
    return is_reply_to


def detect_language(text):
    return langid.classify(text)[0]


def text_get_sentiment(text):
    sentimentanalyse = sentiment(text)
    polarity = sentimentanalyse[0]
    return polarity


def load_text(txt_path):
    with open(txt_path, 'r', encoding="utf-8") as txtf:
        content = txtf.read()
    return content


def chunk_list(ls, n):
    ls = list(zip(*[iter(ls)] * n))
    return ls


def read_csv(input_file, delimiter="\t", encoding='cp1252', has_header=True, keep_header=False, lists=False):
    entry_list = []
    with open(input_file, 'r', encoding=encoding) as f:
        text = f.read()
    rows = text.split('\n')

    if lists:
        rows = [r.split('\t') for r in rows]
        if not keep_header:
            del rows[0]
        del rows[-1]
        return rows

    row_cols = []  # the structure that is to contain the column values by row
    for r in rows:
        row_cols.append(r.split(delimiter))

    # keep track of headers (=dict keys) seperately
    if has_header:
        headers = row_cols[0].copy()
        # 41 headers __________________________________________________
        del row_cols[0]
    else:
        headers = []
        max_row_len = 0
        for entry in row_cols:
            if len(entry) > max_row_len:
                max_row_len = len(entry)
        for i in range(max_row_len):
            headers.append('param_'+str(i+1))

    # iterate entries
    for entry in row_cols:
        update_dict = {}

        # iterate parameters of entry
        for ind, val in enumerate(entry):
            param = headers[ind]  # get the parameter name from the headers
            update_dict[param] = val  # use parameter name as key in the dictionary that represents the status update

        # add the status update to status_updates
        entry_list.append(update_dict)

    if keep_header:
        entry_list.insert(0, headers)
    return entry_list


def read_thread_dataset(tsv_file):
    data = read_csv(tsv_file, encoding='UTF-8', has_header=True, keep_header=True)
    company_dict = {}
    count = 0
    conversation_ids = set()
    for thread in data[1:-1]:
        count += 1
        try:
            if thread['Company'] in company_dict:
                company_dict[thread['Company']] += 1
            else:
                company_dict[thread['Company']] = 1
            conversation_ids.add(thread['Thread_id'])
        except KeyError:
            print('error at: ' + str(count))
    next_id = count + 1

    return data, company_dict, next_id, conversation_ids, data[0]
