# generic functions

"""
    pulls the different slates based on the date and the site
    date- date of the event 
    site- defaults to Draftkings=20, Fanduel=2
    sport- filters the slate by sport, defaults to None
    slate_type- fitlers on the type of contest, Classic by default
"""
sport_mapping = {"football": 1, "baseball": 2, "basketball": 3}


def get_slates(date, site="20", sport="baseball", slate_type="Classic"):
    slate = SLATES.replace("DATE", date).replace("SITE", site)
    slate_data = requests.get(slate).json()
    if sport is not None:
        slate_data = [
            slate for slate in slate_data if slate["sport"] == sport_mapping[sport]
        ]
    if slate_type is not None:
        slate_data = [
            slate for slate in slate_data if slate["slateTypeName"] == slate_type
        ]
    return slate_data


"""
    Fetches the ownerships for a particular slate. Returns the data as a dictionary of players 
    with individual contest ownership after
    slate_id - id of the slate found with the get_slates function
    returns daily_ownerships dict
"""


def get_contest_ownerships(slate_id):
    contest_ownership_url = CONTEST_OWNERSHIP.replace("SLATEID", slate_id)
    daily_ownerships = requests.get(contest_ownership_url).json()
    return daily_ownerships


"""
    Fetches the contests from the slate on that day.
    slate_id -- id of the slate to find contests for
    returns contests in that slate
"""


def get_contests_from_slate(slate_id):
    contests_in_slate_url = CONTEST_SLATE.replace("SLATEID", slate_id)
    contests_in_slate = requests.get(contests_in_slate_url).json()
    return contests_in_slate


"""
    Fetches the lineups 25 at a time based on the contest_id and index passed
    contest_id- id of the contest to fetch (found in the summary call)
    index- index of the lineups to fetch (fetches number 25*(index) - 25*(index+1))
    returns lineups
"""


def get_contest_lineups(contest_id, index=0):
    contest_lineup_url = CONTEST_LINEUPS.replace("CONTESTID", contest_id)
    daily_lineups = requests.get(contest_lineup_url).json()
    return daily_lineups


"""
Maps the contest slates to the 4 different tier buckets
returns the list of contests ids related in their respective buckets
"""


def get_tiers(contests_in_slate, date):
    double_ups = filter((lambda x: "Double Up" in x["name"]), contests_in_slate)
    double_ups = [(contest["_id"], contest["maxEntries"]) for contest in double_ups]
    low_tier = [
        (contest["_id"], contest["maxEntries"])
        for contest in contests_in_slate
        if contest["entryFee"] <= 7
    ]
    mid_tier = [
        (contest["_id"], contest["maxEntries"])
        for contest in contests_in_slate
        if (contest["entryFee"] > 7 and contest["entryFee"] < 25)
    ]
    high_tier = [
        (contest["_id"], contest["maxEntries"])
        for contest in contests_in_slate
        if contest["entryFee"] >= 25
    ]

    low_tier = [x for x in low_tier if x not in double_ups]
    mid_tier = [x for x in mid_tier if x not in double_ups]
    high_tier = [x for x in high_tier if x not in double_ups]
    return [double_ups, low_tier, mid_tier, high_tier, date]


"""
Calculate average ownerships for each tier
returns the average ownership of a player in each tier
    contest_in_slate: contests in the days slate, contains the ownership data
    player_data: players that are available on that slate
return list of average ownership of each player in the 4 tiers (high, med, low, doubleups)
"""


def calculate_tiers(contests_in_slate, player_data):
    double_ups = filter((lambda x: "Double Up" in x["name"]), contests_in_slate)
    double_ups = [contest["name"] for contest in double_ups]

    low_tier = [
        contest["name"] for contest in contests_in_slate if contest["entryFee"] <= 7
    ]
    mid_tier = [
        contest["name"]
        for contest in contests_in_slate
        if (contest["entryFee"] > 7 and contest["entryFee"] < 25)
    ]
    high_tier = [
        contest["name"] for contest in contests_in_slate if contest["entryFee"] >= 25
    ]

    low_tier = [x for x in low_tier if x not in double_ups]
    mid_tier = [x for x in mid_tier if x not in double_ups]
    high_tier = [x for x in high_tier if x not in double_ups]

    low_tier_ownerships = [
        player_data.get(contest_name, 0) for contest_name in low_tier
    ]
    mid_tier_ownerships = [
        player_data.get(contest_name, 0) for contest_name in mid_tier
    ]
    high_tier_ownerships = [
        player_data.get(contest_name, 0) for contest_name in high_tier
    ]
    double_ups_ownerships = [
        player_data.get(contest_name, 0) for contest_name in double_ups
    ]

    if len(low_tier_ownerships) != 0:
        average_low_tier = round(sum(low_tier_ownerships) / len(low_tier_ownerships), 4)
    else:
        average_low_tier = 0
    if len(mid_tier_ownerships) != 0:
        average_mid_tier = round(sum(mid_tier_ownerships) / len(mid_tier_ownerships), 4)
    else:
        average_mid_tier = 0
    if len(high_tier_ownerships) != 0:
        average_high_tier = round(
            sum(high_tier_ownerships) / len(high_tier_ownerships), 4
        )
    else:
        average_high_tier = 0
    if len(double_ups_ownerships) != 0:
        average_double_ups = round(
            sum(double_ups_ownerships) / len(double_ups_ownerships), 4
        )
    else:
        average_double_ups = 0

    return [average_low_tier, average_mid_tier, average_high_tier, average_double_ups]


###############################
#       Helper Functions      #
###############################
def create_rows(lineups, date, contest_id, tier):
    rows = []
    for i in range(0, len(lineups)):
        rows.append(
            [lineups[i]["siteScreenName"], lineups[i]["points"], lineups[i]["rank"]]
            + parse_positions(lineups[i]["lineup"])
            + [date, contest_id, tier]
        )
    return rows


def get_value(entry, pos, num):
    try:
        return entry[pos][num]["name"]
    except:
        return ""


def parse_positions(entry):
    try:
        return [
            get_value(entry, "P", 0),
            get_value(entry, "P", 1),
            get_value(entry, "C", 0),
            get_value(entry, "1B", 0),
            get_value(entry, "2B", 0),
            get_value(entry, "3B", 0),
            get_value(entry, "SS", 0),
            get_value(entry, "OF", 0),
            get_value(entry, "OF", 1),
            get_value(entry, "OF", 2),
        ]
    except IndexError:
        pass

