###############################################################################
# simple_html_scrape.py
# Author: Sunjay Bhatia
# 9/29/2015
#
# Scrape a webpage for all its img tags and download each image
###############################################################################

from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib
import sys

def make_soup(url):
    """Open a url and return BeautifulSoup object of the html source"""

    html = urlopen(url).read()
    return BeautifulSoup(html, "html.parser")


def main():
    # get the url, default to google homepage
    url = 'https://www.google.com'
    if len(sys.argv) > 1:
        url = sys.argv[1]

    soup = make_soup(url)
    for img in soup.find_all('img'):
        src = img.get('src')
        # some error checking so we get image sources in a good format
        if not src or not (src.startswith('/') or src.startswith('http')):
            continue
        # get the file name
        img_name = src.split('/')[-1].split('&')[0].split('?')[0]
        # build the url to download from
        img_url = src if src.startswith('http') else url+src
        print 'Downloading: '+img_url
        urllib.urlretrieve(img_url, img_name)


if __name__ == '__main__':
    main()
