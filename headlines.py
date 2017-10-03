# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 17:51:48 2017

@author: Lenovo
"""
import datetime
import feedparser
from flask import make_response
from flask import Flask
from flask import render_template
from flask import request
import json
from urllib.request import urlopen
from urllib.parse import quote


app = Flask(__name__)

RSS_FEEDS = {'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
             'cnn': "http://rss.cnn.com/rss/edition.rss",
             'fox': "http://feeds.foxnews.com/foxnews/latest",
             'iol': "http://www.iol.co.za/cmlink/1.640"}
DEFAULTS = {'publication':'bbc',
            'city': 'London, UK',
            'currency_from': 'GBP',
            'currency_to': 'USD'}
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=350df53cccf4055b146095d5b4605668"
CURRENCY_URL =  "https://openexchangerates.org//api/latest.json?app_id=e9b019e9e4694caf980313133ace917d"

@app.route("/")
def home():
    #get customized headlines, based on user inputs or default
    publication = get_value_with_fallback('publication')
    articles = get_news(publication)
    
    # get customized weather baased on user input or default
    city = get_value_with_fallback('city')
    weather = get_weather(city)
    
    # get customized currency based on user input or default
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)
    
    # save cookies and return template
    response = make_response(render_template("home.html", articles=articles, weather=weather, currency_from=currency_from,
                           currency_to=currency_to, rate=rate, currencies = sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response

def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    #first_article = feed['entries'][0]
    return feed['entries']

def get_weather(query):
    #api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=350df53cccf4055b146095d5b4605668"
    query = quote(query)  #to sub spaces in query for %20
    url = WEATHER_URL.format(query)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"],
                   'country': parsed['sys']['country']}
    return weather

def get_rate(frm, to):
    all_currency = urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate/frm_rate, parsed.keys())

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    
    
#APIkey 350df53cccf4055b146095d5b4605668
#curr e9b019e9e4694caf980313133ace917d