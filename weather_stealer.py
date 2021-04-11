# encoding=utf8
import unicodedata
import requests
from lxml import html
import mechanize
import time

# Store as (Province, City): (Time, Weather)
weather_cache = {}

def convert_accents(s): 
    # There's an inefficiency here, where we convert the incoming string to UTF-8, so that we know what encoding it's
    # in, and can decode it without causing problems.
    if not s.__class__ == unicode:
        unis = s.decode("utf-8")
    else:
        unis = s

    return unicodedata.normalize('NFD', unis).encode('ascii', 'ignore')

def get_weather_page(city, province):
    """
    City must be a string, containing the city's name.

    Province can just be a two letter string with the province code in it.
    Ex: "QC"

    If you're lazy, the strings can be copy pasted from:
    https://weather.gc.ca/forecast/canada/index_e.html?id=QC
    """
    browser = mechanize.Browser()
    browser.open("https://weather.gc.ca/forecast/canada/index_e.html?id=" + province.upper())

    for i in browser.links():
        if convert_accents(i.text).lower() == convert_accents(city).lower():
            return browser.follow_link(i).read()

    raise requests.exceptions.HTTPError(404)

def check_weather(city, province):
    """
    City must be a string, containing the city's name.

    Province can just be a two letter string with the province code in it.
    Ex: "QC"

    If you're lazy, the strings can be copy pasted from:
    https://weather.gc.ca/forecast/canada/index_e.html?id=QC
    """
    if (province, city) in weather_cache:
        if  time.time() - weather_cache[(province, city)][0] <= 60:
            print("Returning cached weather")
            return weather_cache[(province, city)][1]

    page_content = get_weather_page(city, province)
    page = html.fromstring(page_content)
    desc = page.xpath("//dd[@class=\"mrgn-bttm-0\"]/text()")
    desc += page.xpath("//dd[@class=\"mrgn-bttm-0 wxo-metric-hide\"]/text()")
    wind = page.xpath("//dd[@class=\"longContent mrgn-bttm-0 wxo-metric-hide\"]/text()")
    organized_description = {
        "condition": desc[2],
        "temperature":  float(desc[27].replace(u"\xb0", '')),
        "humidity": desc[4],
        "wind": wind[1] + "km/h"

        }

    weather_cache[(province, city)] = (time.time(), organized_description)
    print("Caching weather...")

    return organized_description

#print(check_weather("Toronto", "ON"))
