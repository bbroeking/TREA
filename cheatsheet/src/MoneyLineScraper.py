from bs4 import BeautifulSoup
import requests
import itertools
import pandas as pd
from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
list_of_skipped = set()
start_date = date(2019, 3, 28)
end_date = date(2019, 3, 29)
for single_date in daterange(start_date, end_date):

    date = single_date.strftime("%Y%m%d")
    url = "http://www.donbest.com/mlb/odds/money-lines/" + date + ".html"
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    odds = soup.find("div", {"class": "odds_gamesHolder"})
    left_games = soup.find_all("td", {"class":"alignLeft"})
    center_games = soup.find_all("td", {"class":"alignCenter"})
    right_games = soup.find_all("td", {"class":"alignRight"})
    game_count = -1

    df = pd.DataFrame(columns=['Away_Team','Home_Team','Away_Starter','Home_Starter','Start_Time','Away_Final_Score','Home_Final_Score', 'Away_Opening', 'Home_Opening', 'Away_Westgate', 
        'Home_Westgate', 'Away_Mirage', 'Home_Mirage', 'Away_Station', 'Home_Station', 'Away_Pinnacle', 'Home_Pinnacle', 'Away_SIA', 'Home_SIA', 'Away_SBG', 'Home_SBG', 
            'Away_BetUS', 'Home_BetUS', 'Away_BetPhoenix', 'Home_BetPhoenix', 'Away_EasyStreet', 'Home_EasyStreet', 'Away_Bovada', 'Home_Bovada', 'Away_Jazz', 'Home_Jazz',
                'Away_Sportsbet', 'Home_Sportsbet', 'Away_Bookmaker', 'Home_Bookmaker', 'Away_DSI', 'Home_DSI', 'Away_AceSport', 'Home_AceSport'])

    teams = ['Away_Team','Home_Team']
    starter = ['Away_Starter','Home_Starter']
    center_cols = ['Start_Time', 'Away_Final_Score', 'Home_Final_Score']
    sportsbooks = ['Away_Westgate', 'Home_Westgate', 'Away_Mirage', 'Home_Mirage', 'Away_Station', 'Home_Station', 'Away_Pinnacle', 'Home_Pinnacle', 'Away_SIA', 'Home_SIA', 'Away_SBG', 'Home_SBG', 
            'Away_BetUS', 'Home_BetUS', 'Away_BetPhoenix', 'Home_BetPhoenix', 'Away_EasyStreet', 'Home_EasyStreet', 'Away_Bovada', 'Home_Bovada', 'Away_Jazz', 'Home_Jazz',
                'Away_Sportsbet', 'Home_Sportsbet', 'Away_Bookmaker', 'Home_Bookmaker', 'Away_DSI', 'Home_DSI', 'Away_AceSport', 'Home_AceSport']

    ##  Game Time / Score ##
    skip_every_third = 1
    row = 0
    pos = 0
    inc_row = False

    for center in center_games:
        scores = center.find_all("div")
        if skip_every_third % 3 != 0:
            for score in scores:
                df.at[row, center_cols[pos]] = score.text
                pos = pos + 1
            if not inc_row:
                inc_row = True
            else:
                inc_row = False
                row = row + 1
                pos = 0
        skip_every_third = skip_every_third + 1

    ## Starter Names / Team Names / Game Lines ##
    row = 0
    for left in left_games:

        game_count = game_count + 1
        div = left.find_all("div")
        span = left.find_all("span")
        skip = True
        pos = 0
        
        for playername in div:
            if skip:
                skip = False
            else:
                df.at[row, starter[pos]] = playername.text
                pos = pos + 1

        pos = 0
        for teamname in span:
            df.at[row, teams[pos]] = teamname.text
            pos = pos + 1

        first = True
        pos = 0
        for x in range(0, 17):
            lines = right_games[x+(game_count*17)].find_all("div")
            for line in lines:
                if first:
                    away_opening = (line.text)[:-4]
                    home_opening = (line.text)[4:]
                    if "." in away_opening or "." in home_opening:
                        list_of_skipped.add(date)
                        print(list_of_skipped)
                    first = False
                    df.at[row, 'Away_Opening'] = away_opening
                    df.at[row, 'Home_Opening'] = home_opening
                else:
                    df.at[row, sportsbooks[pos]] = line.text
                    pos = pos + 1
        row = row + 1
        df.to_csv('/Users/broeking/projects/TREA/MLBLines/2019/' + date + '.csv', encoding='utf-8', index=False)

while list_of_skipped is not None and list_of_skipped != set():
    print(list_of_skipped)
    date = list_of_skipped.pop()
    url = "http://www.donbest.com/mlb/odds/money-lines/" + date + ".html"
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    odds = soup.find("div", {"class": "odds_gamesHolder"})
    left_games = soup.find_all("td", {"class":"alignLeft"})
    center_games = soup.find_all("td", {"class":"alignCenter"})
    right_games = soup.find_all("td", {"class":"alignRight"})
    game_count = -1

    df = pd.DataFrame(columns=['Away_Team','Home_Team','Away_Starter','Home_Starter','Start_Time','Away_Final_Score','Home_Final_Score', 'Away_Opening', 'Home_Opening', 'Away_Westgate', 
        'Home_Westgate', 'Away_Mirage', 'Home_Mirage', 'Away_Station', 'Home_Station', 'Away_Pinnacle', 'Home_Pinnacle', 'Away_SIA', 'Home_SIA', 'Away_SBG', 'Home_SBG', 
            'Away_BetUS', 'Home_BetUS', 'Away_BetPhoenix', 'Home_BetPhoenix', 'Away_EasyStreet', 'Home_EasyStreet', 'Away_Bovada', 'Home_Bovada', 'Away_Jazz', 'Home_Jazz',
                'Away_Sportsbet', 'Home_Sportsbet', 'Away_Bookmaker', 'Home_Bookmaker', 'Away_DSI', 'Home_DSI', 'Away_AceSport', 'Home_AceSport'])

    teams = ['Away_Team','Home_Team']
    starter = ['Away_Starter','Home_Starter']
    center_cols = ['Start_Time', 'Away_Final_Score', 'Home_Final_Score']
    sportsbooks = ['Away_Westgate', 'Home_Westgate', 'Away_Mirage', 'Home_Mirage', 'Away_Station', 'Home_Station', 'Away_Pinnacle', 'Home_Pinnacle', 'Away_SIA', 'Home_SIA', 'Away_SBG', 'Home_SBG', 
            'Away_BetUS', 'Home_BetUS', 'Away_BetPhoenix', 'Home_BetPhoenix', 'Away_EasyStreet', 'Home_EasyStreet', 'Away_Bovada', 'Home_Bovada', 'Away_Jazz', 'Home_Jazz',
                'Away_Sportsbet', 'Home_Sportsbet', 'Away_Bookmaker', 'Home_Bookmaker', 'Away_DSI', 'Home_DSI', 'Away_AceSport', 'Home_AceSport']

    ##  Game Time / Score ##
    skip_every_third = 1
    row = 0
    pos = 0
    inc_row = False

    for center in center_games:
        scores = center.find_all("div")
        if skip_every_third % 3 != 0:
            for score in scores:
                df.at[row, center_cols[pos]] = score.text
                pos = pos + 1
            if not inc_row:
                inc_row = True
            else:
                inc_row = False
                row = row + 1
                pos = 0
        skip_every_third = skip_every_third + 1

    ## Starter Names / Team Names / Game Lines ##
    row = 0
    for left in left_games:

        game_count = game_count + 1
        div = left.find_all("div")
        span = left.find_all("span")
        skip = True
        pos = 0
        
        for playername in div:
            if skip:
                skip = False
            else:
                df.at[row, starter[pos]] = playername.text
                pos = pos + 1

        pos = 0
        for teamname in span:
            df.at[row, teams[pos]] = teamname.text
            pos = pos + 1

        first = True
        pos = 0
        for x in range(0, 17):
            lines = right_games[x+(game_count*17)].find_all("div")
            for line in lines:
                if first:
                    away_opening = (line.text)[:-4]
                    home_opening = (line.text)[4:]
                    if "." in away_opening or "." in home_opening:
                        list_of_skipped.add(date)
                        continue
                    first = False
                    df.at[row, 'Away_Opening'] = away_opening
                    df.at[row, 'Home_Opening'] = home_opening
                else:
                    df.at[row, sportsbooks[pos]] = line.text
                    pos = pos + 1
        row = row + 1
        df.to_csv('/Users/broeking/projects/TREA/MLBLines/2019/' + date + '.csv', encoding='utf-8', index=False)
