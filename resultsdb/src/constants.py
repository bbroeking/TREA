# Static values

# MLB Season Start and End Dates
start_date17 = date(2017, 4, 2)
end_date17 = date(2017, 10, 2)  # Ended Oct. 1

start_date18 = date(2018, 3, 29)
end_date18 = date(2018, 10, 2)  # Ended Oct. 1

start_date19 = date(2019, 3, 20)
end_date19 = date(2019, 9, 30)  # Ended Sept. 29

# NBA Season Start and End Dates
nba_start_date2018 = date(2018, 10, 15)  # nba 2018-19
nba_end_date2018 = date(2019, 4, 10)


class constants:
    # Date format MM/DD/YYYY
    # Site DK=20 FD=2
    SITE = "20"
    # Vars -- DATE, SITE
    # This one can be used to get the player salaries
    SLATES = "https://resultsdb-api.rotogrinders.com/api/slates?start=DATE&site=SITE"
    # Vars -- SLATEID
    CONTEST_OWNERSHIP = (
        "https://resultsdb-api.rotogrinders.com/api/contest-ownership?_slateId=SLATEID"
    )
    # Vars -- CONTESTID, INDEXNUM
    CONTEST_LINEUPS = "https://resultsdb-api.rotogrinders.com/api/entries?_contestId=CONTESTID&sortBy=points&order=desc&index=INDEXNUM&maxFinish=58750&players=&users=false&username=&isLive=false&minPoints=&maxSalaryUsed=&incomplete=false&positionsRemaining=&requiredStartingPositions="
    # Vars SLATEID
    CONTEST_SLATE = (
        "https://resultsdb-api.rotogrinders.com/api/contests?slates=SLATEID&lean=true"
    )
    # Vars -- SLATEID (get summary)
    SUMMARY = ""
