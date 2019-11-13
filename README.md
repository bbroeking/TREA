# TREA

Goal? --> Build an edge over other daily fantasy players

# Player Specific Classification

Classify Player --> projections, matchups, etc --> pretty explored, mostly available to people who hard enough

how many homers is player x projected to hit tonight against pitcher y

Pete Alonso is going to hit more homers against Dylan Bundy than Max Schezer

Less explored --> Statcast metrics + classic metrics

Pete does really well agsint 90-93 mph fastballs, clayton Kershaw throws fastballs of that speed
-> maybe theres an edge to be gained here, because due to kershaw name recognition, pete will not be very heavily played

adding to the weight of a player on a certain night due to performing well in one of these metric categories we create.

---

OUTPUT - Player value --> the scraped projection [a csv with the "value" ofthe player on that day, (Rizzo, 8.6)]

# Lineup Composition / Risk Management / Asset Allocation

## TODO: Lineup analysis

    * Finish scraping the lineups. (a little concerned here, because when we scrape from resultsdb, we dont get more than like 50 entries per contest. we have alot of this data anyways, ill upload it and see if we need to clean it)

    * We can do an analysis of what we think of the lineups/ who the top players are / which players are "winning" people the most money, etc. (indentifiying trends, just familiar with the data / SQL )

Theres 2% of players who win something like 60% of the money on the sites

we have to determine the best way to create these lineups.

e.g. is it ever worth it to player players from more than 4-5 teams in a single lineup?

Say we have 100 lineups --> how to we correctly allocate these lineups

For example

CHC vs PIT (Trevor Williams)

Rizzo %
Happ %
Castelleanos %
Bryant %
Robel %
Schwarber %
Zobrist %
Caratini %
Heyward %

---

OUTPUT - Lineups

# Monte Carlo

Given are projections and the salaries, we can simulate the slate 100000000 times,
and determien the best allocation possible
