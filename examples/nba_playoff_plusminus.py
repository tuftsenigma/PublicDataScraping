###############################################################################
# nba_playoff_plusminus.py
# Author: Sunjay Bhatia
# 9/28/2015
#
# Scrape an NBA player's plus minus for each playing period for each game in
# a given playoff year from basketball-reference.com, aggregate them, and
# plot them if plotly is installed, else output as CSV
# If the player did not participate in the playoffs that year, program exits
# and signals failure
###############################################################################

from __future__ import print_function
from __future__ import division
import sys
import re
import math
from bs4 import BeautifulSoup
from urllib2 import urlopen
try:
    import plotly.plotly as py
    from plotly.graph_objs import *
    do_plot = False
except:
    print('Plot.ly not installed/initialized, to do so run "pip install plotly", and sign up for an account')
    do_plot = False

PLAYER_PROFILE_URL = 'http://www.basketball-reference.com/players/%s/%s.html'
PLAYER_PLAYOFF_URL = 'http://www.basketball-reference.com/players/%s/%s/gamelog/%s/'
GAME_PLUSMINUS_URL = 'http://www.basketball-reference.com/boxscores/plus-minus/%s.html'
GAME_PLUSMINUS_DIV_WIDTH = 1004
GAME_BOXSCORE_COLUMNS = 6
GAME_LENGTH_MINS = 48
GAME_OVERTIME_LENGTH_MINS = 5


def make_soup(url):
    """Open a url and return BeautifulSoup object of the html source"""

    html = urlopen(url).read()
    return BeautifulSoup(html, "html.parser")


def get_player_name(player_id):
    """Given a player's id, get the full name that is listed on their player profile"""

    soup = make_soup(PLAYER_PROFILE_URL % (player_id[0], player_id))
    image_offset_div = soup.find_all('div', {'class': 'person_image_offset'})
    if image_offset_div:
        return image_offset_div[0].h1.string
    else:
        return soup.find_all('div', {'id': 'info_box'})[0].h1.string


def get_playoff_games(player_id, year):
    """
    Given a player id and year, get the playoff game dates and home team
    If the table does not exist, print error and exit
    """

    # get table
    soup = make_soup(PLAYER_PLAYOFF_URL % (player_id[0], player_id, year))
    playoff_table = soup.find(id='pgl_basic_playoffs')
    if not playoff_table:
        print('ERROR: Invalid player/year', file=sys.stderr)
        sys.exit(1)

    # get dates and home teams for each game in a list of tuples
    games = []
    for tr in playoff_table.tbody.find_all('tr', {'id': lambda id: id and id.startswith('pgl_basic_playoffs')}):
        tds = tr.find_all('td')
        date = tds[2].a.string
        if tds[5].string == '@':
            home_team = tds[6].a.string
        else:
            home_team = tds[4].a.string
        games.append((date, home_team))
        
    return games


def get_game_plusminus(player_name, date, home_team):
    """
    Get the plus/minus splits for each time player was in a game
    Returned as list of tuples of form (+/-, start time, end time)
    """

    soup = make_soup(GAME_PLUSMINUS_URL % (date.replace('-','')+'0'+home_team))
    plusminus_div = None
    divs = soup.find_all('div')
    for i, div in enumerate(divs):
        if div.span and div.span.string == player_name:
            plusminus_div = divs[i+1]
            break

    # return None if the player doesn't have plus/minus stats
    if not plusminus_div:
        return None

    # get length of game (check if there are overtime periods)
    columns = soup.find_all('table', {'class': ['nav_table', 'stats_table']})[1].find_all('tr')[1].find_all('th')
    full_game_length_mins = GAME_LENGTH_MINS+(len(columns)-GAME_BOXSCORE_COLUMNS)*GAME_OVERTIME_LENGTH_MINS

    game_plusminuses = []
    curr_width = 0
    for div in plusminus_div.find_all('div'):
        width = int(re.search('\d+', div.get('style')).group(0))
        start_time = (curr_width/GAME_PLUSMINUS_DIV_WIDTH)*full_game_length_mins
        end_time = ((curr_width+width)/GAME_PLUSMINUS_DIV_WIDTH)*full_game_length_mins
        curr_width += width
        if div.string.strip() != '':
            game_plusminuses.append((int(div.string), math.floor(start_time), math.ceil(end_time)))
    
    return game_plusminuses


def plot(pm_info, player_name, player_id, year):
    """Use Plot.ly to plot data if plotly module is installed"""

    data = []
    for pm in pm_info:
        for p in pm:
            data.append(Scatter(
                            x=[p[1], p[2]],
                            y=[p[0], p[0]],
                            mode='lines+markers',
                            line=Line(
                                    color='green' if p[0] > 0 else 'red'
                                )
                        ))

    data = Data(data)
    layout = Layout(
        title=player_name+' '+year+' Playoffs Plus/Minus',
        showlegend=False,
        xaxis=XAxis(
            title='Game minutes'
        ),
        yaxis=YAxis(
            title='Plus/Minus (points)'
        )
    )
    fig = Figure(data=data, layout=layout)
    unique_url = py.plot(fig, filename=player_id+'-'+year+'playoffs-'+'plusminus')

    print('Plot.ly URL: '+unique_url)


def main():
    # argument handling
    if len(sys.argv) != 3:
        print('ERROR: Incorrect usage, should be: python '+sys.argv[0]+' <player_id> <year>',
              file=sys.stderr)
        sys.exit(1)

    player_name = get_player_name(sys.argv[1])

    data = []
    for (date, home_team) in get_playoff_games(sys.argv[1], sys.argv[2]):
        pm = get_game_plusminus(player_name, date, home_team)
        if pm:
            data.append(pm)

    if do_plot:
        plot(data, player_name, sys.argv[1], sys.argv[2])
    else:
        # print in csv format to stdout
        print(player_name+' '+sys.argv[2]+' Playoffs Plus/Minus')
        print('+/-,Start Time,End Time')
        for dt in data:
            for d in dt:
                print(','.join(list([str(x) for x in d])))


if __name__ == '__main__':
    main()
