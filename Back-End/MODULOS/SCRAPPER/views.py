from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

from MODULOS.SCRAPPER.models import *

from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
from newspaper import Article

import pandas as pd
import logging
import time



def APIRequest(request,lang,word):
	template="""
	<div id="entry">
		<h1 id="word">{}</h1>
		<h5 id="definition">{}</h5>
	</div>
	"""

	url = word.replace('@', '/')
	text, title = crawl_link_article(url)
	text = text.lower().replace('[^A-Za-z0-9\s]', '').replace('\n', '').replace('\s+', ' ')

	df = pd.DataFrame({'clean_news': [text]})
	stop = stopwords.words('english')
	df['clean_news'] = df['clean_news'].apply(lambda x: " ".join([word for word in x.split() if word not in stop]))

	tokenizer = Tokenizer()
	tokenizer.fit_on_texts(df['clean_news'])
	sequences = tokenizer.texts_to_sequences(df['clean_news'])
	padded_seq = pad_sequences(sequences, maxlen=500, padding='post', truncating='post')

	model = load_model('/Users/zch/Desktop/m1.h5')
	result = model.predict(padded_seq)
	print(result)
	return HttpResponse(template.format("Title:" + title, "The rate of fake news: " + str(round(result[0][0]*100, 2))+'%'))




def crawl_link_article(url):
    result_json = None
    visible_text = 0
    try:
        if 'http' not in url:
            if url[0] == '/':
                url = url[1:]
            try:
                article = Article('http://' + url)
                article.download()
                time.sleep(2)
                article.parse()
                flag = True
            except:
                logging.exception("Exception in getting data from url {}".format(url))
                flag = False
                pass
            if flag == False:
                try:
                    article = Article('https://' + url)
                    article.download()
                    time.sleep(2)
                    article.parse()
                    flag = True
                except:
                    logging.exception("Exception in getting data from url {}".format(url))
                    flag = False
                    pass
            if flag == False:
                return None
        else:
            try:
                article = Article(url)
                article.download()
                time.sleep(2)
                article.parse()
            except:
                logging.exception("Exception in getting data from url {}".format(url))
                return None

        if not article.is_parsed:
            return None

        visible_text = article.text
        top_image = article.top_image
        images = article.images
        keywords = article.keywords
        authors = article.authors
        canonical_link = article.canonical_link
        title = article.title
        meta_data = article.meta_data
        movies = article.movies
        publish_date = article.publish_date
        source = article.source_url
        summary = article.summary

        result_json = {'url': url, 'text': visible_text, 'images': list(images), 'top_img': top_image,
                       'keywords': keywords,
                       'authors': authors, 'canonical_link': canonical_link, 'title': title, 'meta_data': meta_data,
                       'movies': movies, 'source': source,
                       'summary': summary}
    except:
        logging.exception("Exception in fetching article form URL : {}".format(url))

    return visible_text, title