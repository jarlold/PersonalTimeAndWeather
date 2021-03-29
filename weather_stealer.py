# encoding=utf8
import unicodedata
import requests
from lxml import html
import mechanize


def get_weather_page(city, province):
    """
    City must be a unicde string, containing the city's accents, and capitalization
    Ex: u"Pointe-à-la-Croix"

    Province can just be a two letter string with the province code in it.
    Ex: "QC"

    If you're lazy, the strings can be copy pasted from:
    https://weather.gc.ca/forecast/canada/index_e.html?id=QC
    """
    browser = mechanize.Browser()
    browser.open("https://weather.gc.ca/forecast/canada/index_e.html?id=" + province)

    return browser.follow_link(text_regex=city).read()
    

def check_weather(city, province):
    """
    City must be a unicde string, containing the city's accents, and capitalization
    Ex: u"Pointe-à-la-Croix"

    Province can just be a two letter string with the province code in it.
    Ex: "QC"

    If you're lazy, the strings can be copy pasted from:
    https://weather.gc.ca/forecast/canada/index_e.html?id=QC
    """
    #page_content = requests.get("https://weather.gc.ca/city/pages/qc-147_metric_e.html").content
    page_content = get_weather_page(city, province)
    page = html.fromstring(page_content)
    return page.xpath("//dd[@class=\"mrgn-bttm-0\"]/text()")[2]



print(check_weather(u"Montréal", "QC"))
