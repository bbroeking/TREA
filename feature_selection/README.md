Organization of the data on BigQuery

1.  X and X+1 creates the statcast_by_inning201\*
    This query will create rows with all data from inning X and the 0/1 result of a run being scored in
    the next inning

2.  GenerateBattingOrder creates the batting_order201\*
    Groups the data by batter in each game, and each inning. This will give us the at_number of each batter
    in an inning
    (might be ignoring the case where one hitter will bat twice, but just a small inconsistancy, maybe use
    MIN not MAX to solve this?)

3.  SelectFirst3Batters create the order_number201\*
    This filters out each inning such that we only have the first three batters in each

4.  JoinFirstThree creates the order201\*
    joins the three different rows created in the previous step into one, it might be more efficient
    to do it some other way

5.  Next3 creates the batting_order_by_inning201\*
    combine the query from (1) with the data from (4) to be able to tell who the next 3 batters due up are
