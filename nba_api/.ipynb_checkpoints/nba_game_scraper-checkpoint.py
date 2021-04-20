import pandas as pd

from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder


# get team IDs
team_dict = teams.get_teams()





# get scores

## inputs
from_dt = '09/01/2015'
to_dt = '01/20/2021'
nba = '00'


scores_df = (leaguegamefinder.LeagueGameFinder(date_from_nullable = from_dt, 
                                               date_to_nullable = to_dt,
                                               season_type_nullable = 'Regular Season',
                                               league_id_nullable	= nba)
             .get_data_frames()[0])


scores_df.to_csv('/Users/markusfiordaliso/Documents/coding_projects/sports_bet/nba/data/nba_scores_20150901_20210120.csv', index = False)

