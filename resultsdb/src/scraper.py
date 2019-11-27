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


def export_tiered_contest_lineups():
    pass


def export_contest_lineups(date):
    import itertools

    resultsdb_date = date.strftime("%m/%d/%Y")
    date = date.strftime("%Y-%m-%d")
    daily_slate = get_slates(resultsdb_date, SITE, sport="baseball")
    slate_dataframes = []
    for slate in daily_slate:
        slate_id = slate["_id"]
        contests_in_slate = get_contests_from_slate(slate_id)
        tiers = get_tiers(contests_in_slate)
        for tier in range(0, len(tiers)):
            lineups_in_tier = get_lineups_in_tier(tiers[tier], date, tier)
            lineups_in_tier = list(itertools.chain.from_iterable(lineups_in_tier))
            columns = [
                "username",
                "points",
                "contest_rank",
                "P1",
                "P2",
                "C",
                "1B",
                "2B",
                "3B",
                "SS",
                "OF1",
                "OF2",
                "OF3",
                "date",
                "contest_id",
                "tier",
            ]
            df = pd.DataFrame(lineups_in_tier, columns=columns)
            df = df.drop_duplicates()
            slate_dataframes.append(df)
    return slate_dataframes


def get_lineups_in_tier(tier, date, tier_level):
    lineups_in_tier = []
    for contest in tier:
        max_intervals = min(20, int(contest[1] / 25) + (contest[1] % 25 > 0))
        for interval in range(0, max_intervals):
            contest_lineups = get_contest_lineups(contest[0], interval)
            if len(contest_lineups) == 0:
                continue
            entries = contest_lineups["entries"]
            created_rows = create_rows(entries, date, contest[0], tier_level)
            lineups_in_tier.append(created_rows)
    return lineups_in_tier


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


# eg ../data/resultsdb/TierContestsBasketball/2019/{}-ownerships-{}.csv
def export_tiered_contest_ownerships(daily_slate, export_path):
    for slate in daily_slate:
        SLATEID = slate["_id"]
        # skip slates where gameCount < 5
        #         if slate.get('gameCount', 0) < 5:
        #             continue
        # Get the names of the contests in the slate
        contests_in_slate = get_contests_from_slate(SLATEID)
        contest_names = [contest["name"] for contest in contests_in_slate]
        # Fetch daily ownerships
        daily_ownerships = get_contest_ownerships(SLATEID)
        # Parse data into a list to add to dataframe
        appended_player_data = []
        for player in daily_ownerships:
            player_data = daily_ownerships[player]
            player_row = [
                player_data.get("name", None),
                player_data.get("slatePosition", None),
                player_data.get("salary", None),
                player_data.get("actualFpts", 0),
                player_data.get("projectedFpts", 0),
                player_data.get("projectedOwnership", 0),
                round(player_data.get("combinedOwnership", 0), 4),
            ]
            player_contest_row = calculate_tiers(contests_in_slate, player_data)
            joined_list = player_row + player_contest_row + [date] + [SLATEID]
            appended_player_data.append(joined_list)
        # Create table structure from the data
        df = pd.DataFrame(
            appended_player_data,
            columns=[
                "name",
                "slatePosition",
                "salary",
                "actualFpts",
                "projectedFpts",
                "projectedOwnership",
                "combinedOwnership",
                "low_tier",
                "mid_tier",
                "high_tier",
                "double_ups",
                "date",
                "slate_id",
            ],
        )
        df.to_csv(export_path.format(date, SLATEID))


def get_tiers(contests_in_slate):
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
    return [double_ups, low_tier, mid_tier, high_tier]

"""
Calculate Tiers
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
