import os
import pickle as pkl
import pandas as pd
import re
import nltk
from nltk.tokenize import wordpunct_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier

PKL_MODEL = 'model.pkl'

regex_pattern1 = r'#[\w]*'
regex_pattern2 = r'@[\w]*'
emoticon_list = {':))': 'positive_emoticon', ':)': 'positive_emoticon', ':D': 'positive_emoticon',
                 ':(': 'negative_emoticon', ':((': 'negative_emoticon', '8)': 'neutral_emoticon'}

std_list = {'eh': 'é', 'vc': 'você', 'vcs': 'vocês', 'tb': 'também', 'tbm': 'também', 'obg': 'obrigado',
            'gnt': 'gente',
            'q': 'que', 'k': 'que', 'n': 'não', 'cmg': 'comigo', 'p': 'para', 'ta': 'está', 'to': 'estou',
            'vdd': 'verdade'}

nltk_stopwords = nltk.corpus.stopwords.words('portuguese')

vectorizer, tfidf_transformer, model = None, None, None


def remove_url(data):
    ls = []
    regexp1 = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    regexp2 = re.compile('www?.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    for line in data:
        urls = regexp1.findall(line)

        for u in urls:
            line = line.replace(u, ' ')

        urls = regexp2.findall(line)

        for u in urls:
            line = line.replace(u, ' ')

        ls.append(line)
    return ls


def remove_regex(data, regex_pattern):
    ls = []

    for line in data:
        matches = re.finditer(regex_pattern, line)

        for m in matches:
            line = line.replace(m.group().strip(), '')

        ls.append(line)

    return ls


def replace_emoticons(data, emoticon_list):
    ls = []

    for line in data:
        for exp in emoticon_list:
            line = line.replace(exp, emoticon_list[exp])

        ls.append(line)

    return ls


def tokenize_text(data):
    # ls = []
    #
    # for line in data:
    #     tokens = wordpunct_tokenize(line)
    #     ls.append(tokens)
    #
    # return ls

    return [wordpunct_tokenize(line) for line in data]


def apply_standardization(tokens, std_list):
    ls = []

    for tk_line in tokens:
        new_tokens = []

        for word in tk_line:
            if word.lower() in std_list:
                word = std_list[word.lower()]

            new_tokens.append(word)

        ls.append(new_tokens)

    return ls


def remove_stopwords(tokens, stopword_list):
    ls = []

    for tk_line in tokens:
        new_tokens = []

        for word in tk_line:
            if word.lower() not in stopword_list:
                new_tokens.append(word)

        ls.append(new_tokens)

    return ls


def untokenize_text(tokens):
    ls = []

    for tk_line in tokens:
        new_line = ''

        for word in tk_line:
            new_line += word + ' '

        ls.append(new_line)

    return ls


def _get_accuracy(matrix):
    acc = 0
    n = 0
    total = 0

    for i in range(0, len(matrix)):
        for j in range(0, len(matrix)):
            if i == j:
                n += matrix[i, j]

            total += matrix[i, j]

    acc = n / total
    return acc


def makePrediction(corpus, regex_pattern1=regex_pattern1, regex_pattern2=regex_pattern2, emoticon_list=emoticon_list,
                   std_list=std_list, nltk_stopwords=nltk_stopwords):
    X_new = remove_url(corpus)
    X_new = remove_regex(X_new, regex_pattern1)
    X_new = remove_regex(X_new, regex_pattern2)
    X_new = replace_emoticons(X_new, emoticon_list)
    X_new_tokens = tokenize_text(X_new)
    X_new_tokens = apply_standardization(X_new_tokens, std_list)
    X_new_tokens = remove_stopwords(X_new_tokens, nltk_stopwords)
    X_new = untokenize_text(X_new_tokens)
    X_new_vect = vectorizer.transform(X_new)
    X_new_tfidf = tfidf_transformer.transform(X_new_vect)
    X_new_tfidf = tfidf_transformer.transform(X_new_vect)
    standalone_prediction = model.predict(X_new_tfidf)
    return standalone_prediction[0]


def generate():
    X_col = 'tweet_text'
    y_col = 'sentiment'

    train_ds = pd.read_csv('./../DatasetsTrain/Train3Classes.csv', delimiter=';')
    train_ds[y_col] = train_ds[y_col].map({0: 'Negative', 1: 'Positive', 2: 'Neutral'})
    X_train = train_ds.loc[:, X_col].values
    y_train = train_ds.loc[:, y_col].values

    test_ds = pd.read_csv('./../DatasetsTest/Test3classes.csv', delimiter=';')
    test_ds[y_col] = test_ds[y_col].map({0: 'Negative', 1: 'Positive', 2: 'Neutral'})
    X_test = test_ds.loc[:, X_col].values
    y_test = test_ds.loc[:, y_col].values

    X_train = remove_url(X_train)
    X_test = remove_url(X_test)

    X_train = remove_regex(X_train, regex_pattern1)  # VERY SLOW
    X_test = remove_regex(X_test, regex_pattern1)

    X_train = remove_regex(X_train, regex_pattern2)  # VERY SLOW
    X_test = remove_regex(X_test, regex_pattern2)

    X_train = replace_emoticons(X_train, emoticon_list)
    X_test = replace_emoticons(X_test, emoticon_list)

    X_train_tokens = tokenize_text(X_train)  # VERY SLOW
    X_test_tokens = tokenize_text(X_test)

    X_train_tokens = apply_standardization(X_train_tokens, std_list)
    X_test_tokens = apply_standardization(X_test_tokens, std_list)

    X_train_tokens = remove_stopwords(X_train_tokens, nltk_stopwords)  # SLOW
    X_test_tokens = remove_stopwords(X_test_tokens, nltk_stopwords)

    X_train = untokenize_text(X_train_tokens)
    X_test = untokenize_text(X_test_tokens)

    vectorizer = CountVectorizer()  # Need to load
    X_train_vect = vectorizer.fit_transform(X_train)  # SLOW

    tfidf_transformer = TfidfTransformer()  # Need to load
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_vect)

    model = RandomForestClassifier(max_depth=8)  # Need to load
    model.fit(X_train_tfidf, y_train)  # SLOW

    return vectorizer, tfidf_transformer, model


def load():
    if os.path.exists(PKL_MODEL):
        with open(PKL_MODEL, 'rb') as f:
            return pkl.load(f)
    else:
        data = generate()

        with open(PKL_MODEL, 'wb') as f:
            pkl.dump(data, f)

        return data


vectorizer, tfidf_transformer, model = load()
