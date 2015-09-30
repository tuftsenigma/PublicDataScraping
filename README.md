# PublicDataScraping
Enigma Fall 2015 Workshop 1: Scraping public data sources with python

Used in conjunction with [yotambentov](https://github.com/yotambentov)'s [PyNight2015](https://github.com/yotambentov/PyNight2015) talk at Tufts University

---

### Requirements

* Command line application (e.g. Terminal on OSX/Linux, Command Prompt/Cygwin on Windows)
* Install Python ([OSX](http://docs.python-guide.org/en/latest/starting/install/osx/), [Windows](http://docs.python-guide.org/en/latest/starting/install/win/))
* Install [pip](https://pip.pypa.io/en/latest/installing/)
* Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* Text editor
* Take a look at Yotam's lecture above and get familiar with Python

---

### Getting Started

#### Get the code
Open your terminal application and run the following:

    git clone https://github.com/tuftsenigma/PublicDataScraping.git

#### Install BeautifulSoup
    
    sudo pip install beautifulsoup4

Remove `sudo` on Windows

#### Install yahoo-finance

	pip install yahoo-finance

Remove `sudo` on Windows

---

### Running Examples

#### Scraping the [Tufts Daily](http://tuftsdaily.com) for Links

    python link_scrape_tufts_daily.py

#### Scraping web pages for images

    python simple_html_img_scrape.py [url]

`url` is an optional argument, defaults to [https://google.com](https://google.com)

#### NBA Playoff Plus/Minus
To enable plotting using [Plot.ly](https://plot.ly/), follow the initialization instructions found [here](https://plot.ly/python/getting-started/)

Run the code:

    cd examples
    python nba_playoff_plusminus.py <player_id> <year>

Where the `player_id` is an identifier found from [basketball-reference.com](http://www.basketball-reference.com/) e.g. `iversal01` for Allen Iverson

An example for [J.R. Smith's 2015 Playoffs](https://plot.ly/~sunjayb/68/jr-smith-2015-playoffs-plusminus/)
