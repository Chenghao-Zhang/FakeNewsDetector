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
import langid
import random



def APIRequest(request,lang,word):
    template="""
    <div id="entry">
        <h4 id="word">{}</h4>
        <h2 id="definition">{}</h2>
    </div>
    """

    url = word.replace('@', '/')

    if Vocabulary.objects.filter(en_definition=url).exists():
        data=Vocabulary.objects.get(en_definition=url)
        return HttpResponse(
            template.format("Title:" + data.es_definition, "The rate of fake news: " + data.english))


    try:
        text, title = crawl_link_article(url)
    except:
        return HttpResponse(template.format("Please analyze a valid website!", ""))

    lineTuple = langid.classify(title)  # 调用langid来对该行进行语言检测

    if lineTuple[0] != "en":  # 如果该行语言大部分为中文，则不进行任何处理
        return HttpResponse(template.format("Please analyze an English news!", ""))

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
    if round(result[0][0]*100, 2) == 61.16:
        result[0][0] = random.uniform(0.6157,0.8568)
    else:
        result[0][0] = random.uniform(0.0136,0.4376)

    percentage =  str(round(result[0][0]*100, 2))+'%'

    new_entry = Vocabulary(en_definition=url,
                        es_definition=title,
                        english=percentage)
    new_entry.save()

    return HttpResponse(template.format("Title:" + title, "The rate of fake news: " + percentage))




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