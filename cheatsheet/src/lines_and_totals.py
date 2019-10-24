# Skipping 6.26, 5.25
import fuzzymatcher
import pandas as pd
import os

batters = pd.read_csv("Batters2017.csv")
pitchers = pd.read_csv("Pitchers2017.csv")
min_batters = batters[['Name', 'Team']]
min_pitchers = pitchers[['Name', 'Team']]
df2 = pd.concat([min_batters, min_pitchers])

teams_full = dict()
teams_full["LAA"] = "Los Angeles Angels"	
teams_full["HOU"] = "Houston Astros"
teams_full["OAK"] = "Oakland Athletics"
teams_full["TOR"] = "Toronto Blue Jays"	
teams_full["ATL"] = "Atlanta Braves"	
teams_full["MIL"] = "Milwaukee Brewers"	
teams_full["STL"] = "St. Louis Cardinals"
teams_full["CHC"] = "Chicago Cubs"	
teams_full["ARI"] = "Arizona Diamondbacks"
teams_full["LAD"] = "Los Angeles Dodgers"	
teams_full["SFO"] = "San Francisco Giants"	
teams_full["CLE"] = "Cleveland Indians"	
teams_full["SEA"] = "Seattle Mariners"	
teams_full["MIA"] = "Miami Marlins"	
teams_full["NYM"] = "New York Mets"	
teams_full["WAS"] = "Washington Nationals"	
teams_full["BAL"] = "Baltimore Orioles"	
teams_full["SDG"] = "San Diego Padres"	
teams_full["PHI"] = "Philadelphia Phillies"	
teams_full["PIT"] = "Pittsburgh Pirates"	
teams_full["TEX"] = "Texas Rangers"	
teams_full["TAM"] = "Tampa Bay Rays"	
teams_full["BOS"] = "Boston Red Sox"
teams_full["CIN"] = "Cincinnati Reds"
teams_full["COL"] = "Colorado Rockies"
teams_full["KAN"] = "Kansas City Royals"
teams_full["DET"] = "Detroit Tigers"
teams_full["MIN"] = "Minnesota Twins"
teams_full["CWS"] = "Chicago White Sox"
teams_full["NYY"] = "New York Yankees"

teams = dict()
teams["LAA"] = "Angels"	
teams["HOU"] = "Astros"
teams["OAK"] = "Athletics"
teams["TOR"] = "Blue Jays"	
teams["ATL"] = "Braves"	
teams["MIL"] = "Brewers"	
teams["STL"] = "Cardinals"
teams["CHC"] = "Cubs"
teams["ARI"] = "Diamondbacks"
teams["LAD"] = "Dodgers"	
teams["SFO"] = "Giants"	
teams["CLE"] = "Indians"	
teams["SEA"] = "Mariners"	
teams["MIA"] = "Marlins"	
teams["NYM"] = "Mets"	
teams["WAS"] = "Nationals"	
teams["BAL"] = "Orioles"	
teams["SDG"] = "Padres"	
teams["PHI"] = "Phillies"	
teams["PIT"] = "Pirates"	
teams["TEX"] = "Rangers"	
teams["TAM"] = "Rays"	
teams["BOS"] = "Red Sox"
teams["CIN"] = "Reds"
teams["COL"] = "Rockies"
teams["KAN"] = "Royals"
teams["DET"] = "Tigers"
teams["MIN"] = "Twins"
teams["CWS"] = "White Sox"
teams["NYY"] = "Yankees"

def full_team_map(name):
    if name in teams_full.keys():
        return teams_full[name]
    return name
def team_map(name):
    if name in teams.keys():
        return teams[name]
    return name

rootdir = "/Users/broeking/projects/TREA/merge/Ownership_Salaries"
for directory in os.listdir(rootdir):
    if directory == ".DS_Store":
        continue
    date = rootdir + "/" + directory
    for subdir, dirs, files in os.walk(date):
        for f in files:
            date_to_use = date + "/" + f
            split_date = directory.split(".")
            date_csv = "2017" + split_date[0].zfill(2) + split_date[1].zfill(2) + ".csv"

            try:
                lines = pd.read_csv("../MLBLines/2017/" + date_csv)
                totals = pd.read_csv("../MLBTotals/2017/" + date_csv)
                
                batters_L = pd.read_csv("../splits/2018_batter_vL.csv")
                batters_R = pd.read_csv("../splits/2018_batter_vR.csv")
                pitchers_L = pd.read_csv("../splits/2018_pitcher_vL.csv")
                pitchers_R = pd.read_csv("../splits/2018_pitcher_vR.csv")

            except FileNotFoundError:
                continue

            df = pd.read_csv(date_to_use, thousands=',')
            df['full_name'] = df['Team_right'].apply(full_team_map)
            df['nickname'] = df['Team_right'].apply(team_map)

            away_lines = lines[['Away_Team', 'Away_Opening']]
            home_lines = lines[['Home_Team', 'Home_Opening']]

            away_lines = away_lines.rename(columns={'Away_Team':"Team",
                                                'Away_Opening':"Line"})
            home_lines = home_lines.rename(columns={'Home_Team':"Team",
                                                'Home_Opening':"Line"})
            total_lines = pd.concat([away_lines, home_lines])
            
            df = df.merge(total_lines, left_on="full_name", right_on="Team", how="inner")

            away_totals = totals[["Away_Team", "Total"]]
            home_totals = totals[["Home_Team", "Total"]]
            away_totals = away_totals.rename(columns={'Away_Team':"Team"})
            home_totals = home_totals.rename(columns={'Home_Team':"Team"})
            total_totals = pd.concat([away_totals, home_totals])

            df = df.merge(total_totals, left_on="full_name", right_on="Team", how="inner")

            df = df.rename(columns={"%Drafted_left":"Ownership", "FPTS_left":"FPTS", "Position_right":"Position",
                                    "Points_right":"Points", "Salary_right":"Salary", "Team_right":"Team",
                                    "Order_right":"Order", "Opponent_right":"Opponent", "Name_right":"Name"})
            df = df.drop(columns=['Unnamed: 0', 'Player_left', 'Team_x', 'Team_y'])
            df = df.dropna()

            df_pitcher = df.loc[df['Position'] == "P"]
            df_non_pitcher = df.loc[df['Position'] != "P"]

            print(df_pitcher.head())
            print(pitchers.head())

            left_on=["Name", "nickname"]
            right_on=["Name", "Team"]
            df_pitcher = df_pitcher.merge(pitchers, left_on=left_on, right_on=right_on, how="inner")
            df_non_pitcher = df_non_pitcher.merge(batters, left_on=left_on, right_on=right_on, how="inner")

            if not (os.path.exists(os.getcwd() + "/Ownership_Salaries_Lines_Batters/" + directory)):
                    os.mkdir(os.getcwd() + "/Ownership_Salaries_Lines_Batters/" + directory)
            if not (os.path.exists(os.getcwd() + "/Ownership_Salaries_Lines_Pitchers/" + directory)):
                    os.mkdir(os.getcwd() + "/Ownership_Salaries_Lines_Pitchers/" + directory)
            df_pitcher.to_csv("Ownership_Salaries_Lines_Pitchers/" + directory + "/" + f)
            df_non_pitcher.to_csv("Ownership_Salaries_Lines_Batters/" + directory + "/" + f)

