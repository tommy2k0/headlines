# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 17:51:48 2017

@author: Lenovo
"""
import feedparser
from flask import Flask
from flask import render_template


app = Flask(__name__)

RSS_FEEDS = {'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
             'cnn': "http://rss.cnn.com/rss/edition.rss",
             'fox': "http://feeds.foxnews.com/foxnews/latest",
             'iol': "http://www.iol.co.za/cmlink/1.640"}

@app.route("/")
@app.route("/<publication>")   #< > indicates a variable  which can be allocated dynamicaly based on the url
def get_news(publication="bbc"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    #first_article = feed['entries'][0]
    return render_template("home.html", articles=feed['entries'])

if __name__ == '__main__':
    app.run(port=5000, debug=True)