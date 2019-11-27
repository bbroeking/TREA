# an implementation with the functions
tiers = ["double_ups", "low_tier", "mid_tier", "high_tier"]
for single_date in daterange(start_date, end_date):
    date = single_date.strftime("%Y-%m-%d")
    result = export_contest_lineups(single_date)
    for res in range(0, len(result)):
        if len(result[res]) == 0:
            continue
        else:
            result[res].to_csv(
                "../data/resultsdb/TierLineups/2019/{}-lineups-{}.csv".format(
                    date, random()
                )
            )

