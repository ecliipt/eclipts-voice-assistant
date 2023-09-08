import bs4 as bs
import nltk
import urllib.request
import re

import wikipedia
import random

import utils.logging as logging

def engine(topic):
    """topic=topic.replace(' ', '_')
    scraped_data = urllib.request.urlopen(f'https://en.wikipedia.org/wiki/{topic}')
    article = scraped_data.read()

    parsed_article = bs.BeautifulSoup(article,'lxml')

    disambiguation_template = parsed_article.find_all('div', {'class': 'hatnote navigation-not-searchable'})
    if disambiguation_template:
        # If it is a disambiguation page, raise an error
        raise ValueError(f"{url} is a disambiguation page")

    paragraphs = parsed_article.find_all('p')

    article_text = ""

    for p in paragraphs:
        article_text += p.text

    print(article_text)"""

    topic=topic.replace(' ', '_')
    try:
        article_text = wikipedia.summary(topic)
    except wikipedia.exceptions.DisambiguationError as e:
        logging.warn(f'Disambiguation Error encountered: {e}')
        try:
            topic = random.choice(e.options)
            logging.debug("from Disambiguation options, selected: "+topic)
            article_text = wikipedia.summary(topic)
        except Exception as e:
            logging.fail(e)
            raise ValueError(f'Exception found while trying to handle disambiguation page: "{e}"')
    except wikipedia.exceptions.PageError as e:
        logging.fail(e)
        raise ValueError(f'Could not find anything related to "{topic}" online')

    
    #print(article_text)


    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(article_text)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    import heapq
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = re.sub(r'\([^)]*\)', '', ' '.join(summary_sentences))
    return summary if len(article_text) > len(summary) else re.ub(r'\([^)]*\)', '', article_text)

def main(_input_=None):
    if _input_  == None: raise ValueError('No input data was provided for the search.')
    return engine(_input_)