###############################################################################
# link_scrape_tufts_daily.py
# Author: Sunjay Bhatia
# 9/29/2015
#
# Scrape the Tufts Daily website for each link and link title
###############################################################################

from bs4 import BeautifulSoup
from urllib2 import urlopen

def make_soup(url):
    """Open a url and return BeautifulSoup object of the html source"""

    html = urlopen(url).read()
    return BeautifulSoup(html, "html.parser")


def main():
    soup = make_soup('http://tuftsdaily.com')

    for a in soup.find_all('a'):
        href = a.get('href')
        # make sure there is a link
        if not href:
            continue
        print a.string, href 


if __name__ == '__main__':
    main()
