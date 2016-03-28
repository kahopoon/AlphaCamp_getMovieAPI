#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2, re, json
from threading import Thread
from Queue import Queue

queue = Queue()
result = []

def start():
    movie_list = movieList()
    map(lambda x: queue.put(x), movie_list)
    workers(len(movie_list))

def workers(thread_count):
    NUM_THREADS = thread_count
    threads = map(lambda i: Thread(target=movieData), xrange(NUM_THREADS))
    map(lambda th: th.start(), threads)
    map(lambda th: th.join(), threads)

def movieList():
    movie_list = []
    html_data = urllib2.urlopen("https://movie.yahoo-leisure.hk/movie/showing").read()
    found = re.findall('<div class="each-movie"><a href="/movie/details/' + '(.+?)' + '" class="title">', html_data) 
    if found:
        for row in found:
            movie_list.append(row)
    return movie_list

def movieData():
    movie_data = {}
    while not queue.empty():
        movie_row_url = queue.get()
        movie_row_html_data = urllib2.urlopen("https://movie.yahoo-leisure.hk/movie/details/" + movie_row_url).read()
        movie_cover = re.search('<img src="/assets/poster/' + '(.+?)' + '.jpg"', movie_row_html_data)
        movie_cast = re.findall('<dd class="long">' + '(.+?)' + '</dd>', movie_row_html_data, re.DOTALL)
        movie_director_duration = re.findall('<dd>' + '(.+?)' + '</dd>', movie_row_html_data, re.DOTALL)
        movie_description = re.findall('<p class="description">' + '(.+?)' + '</p>', movie_row_html_data, re.DOTALL)
        movie_data['name'] = movie_row_url[6:]
        movie_data['cast'] = movie_cast[0]
        movie_data['director'] = movie_director_duration[0]
        movie_data['duration'] = movie_director_duration[1]
        movie_data['description'] = movie_description[0]
        movie_data['cover'] = (movie_cover.group(1)).replace("<br \/>\r\n", "")
        movie_data['url'] = movie_row_url[:5]
        if len(movie_data) > 0:
            result.append(movie_data)

def output_json(result):
    return json.dumps(result,ensure_ascii=False)

start()
print output_json(result)
