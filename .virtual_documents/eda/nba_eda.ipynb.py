import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt

# dictionary
import sbr_team_name 


game_df = pd.read_csv('/Users/markusfiordaliso/Documents/coding_projects/pro_sports/nba_basketball/data/nba_scores_20150901_20210120.csv')
odds_df = pd.read_csv('/Users/markusfiordaliso/Documents/coding_projects/pro_sports/nba_basketball/data/nba_odds_20150901_20210120.csv')



# odds_data

## remove unneccasary col
odd_col_keep = ['date', 'away_team', 'home_team', 'pinnacle1', 'pinnacle2']
odds_df = odds_df[odds_df.columns & odd_col_keep]

## date 
odds_df['date'] = pd.to_datetime(odds_df['date'], format = 'get_ipython().run_line_magic("Y%m%d')", "")

## rename book odds
odds_df.rename(columns={'pinnacle1' : 'away_odds', 'pinnacle2' : 'home_odds'}, inplace=True)

## covert text to lower case
odds_df = odds_df.apply(lambda x: x.str.lower() if(x.dtype== 'object') else x)

## restructure to vertical
home_odds = odds_df.iloc[:, [0, 1, 3]]
away_odds = odds_df.iloc[:, [0, 2, 4]]

home_odds.columns = ['date', 'team_name', 'odds']
away_odds.columns = ['date', 'team_name', 'odds']

odds_df = pd.concat([home_odds, away_odds])

## replace period in team name
odds_df['team_name'] = odds_df['team_name'].str.replace('.', '')

## team name cleanup to align to nba api
odds_df = odds_df.replace({'team_name' : sbr_team_name.sbr_dictionary})



# game_df

## covert text to lower case
game_df = game_df.apply(lambda x: x.str.lower() if(x.dtype == 'object') else x)
game_df.columns = map(str.lower, game_df.columns)

## date
game_df['game_date'] = pd.to_datetime(game_df['game_date'])

## add odds. NEED TO FIGURE OUT HOW TO DROP DATE COL AUTOMATICALLY
game_df = (pd
           .merge(game_df, odds_df,
                  left_on=['game_date', 'team_name'], right_on=['date', 'team_name'],
                  how='left',
                  copy=False))

# binary variables
game_df['game_won'] = np.where(game_df['wl'] == 'w', 1, 0)



# home/away
game_df['home_team'] = game_df['matchup'].map(lambda x: 0 if '@' in x else 1)

# playing back to back
game_df = game_df.sort_values(['team_abbreviation', 'game_date'])
game_df['prior_game_date'] = game_df.groupby(['team_abbreviation'], as_index=False)['game_date'].shift(1)
game_df['prior_day_game'] = np.where(game_df['game_date'] - timedelta(days=1) == game_df['prior_game_date'], 1, 0)

# points against
game_df['pts_against'] = game_df['pts'] - game_df['plus_minus']



#correlologram on specific variables...BREAK VAR INTO PRE GAME & IN GAME
corr_pre_game = ['game_won', 'odds', 'home_team', 'prior_day_game']

corr_in_game = ['game_won', 'pts', 'fgm', 'fga', 'fg_pct','fg3m', 'fg3a', 'fg3_pct',
                'ftm', 'fta', 'ft_pct', 'oreb', 'dreb','reb', 'ast', 'stl', 'blk',
                'tov', 'pf', 'plus_minus', 'pts_against']



plt.figure(figsize=(10, 8))
plt.title('Correlation matrix of pre-game variables')

sns.heatmap(game_df.loc[:, corr_pre_game].corr(),
            annot=True,
            fmt = '.1g',
            center = 0,
            vmax=1,
            vmin=-1,
            cmap='RdBu',
            linewidths=0.2)


plt.figure(figsize=(13,10))
plt.title('Correlation matrix of in-game stats')

sns.heatmap(game_df.loc[:, corr_in_game].corr(),
            annot=True,
            fmt = '.1g',
            center = 0,
            vmax=1,
            vmin=-1,
            cmap='RdBu',
            linewidths=0.2)



plt.figure(figsize=(13,10))
plt.xlim(-1500, 1500)
plt.title('NBA Sportsbook Odds - Pinnacle')

sns.histplot(game_df,
             x='odds',
             binwidth=50,
             hue='game_won')


# Create fav/und binary variable and look for groupings

## FIX SPEED OF THIS APPROACH
game_id_group = (game_df
                 .groupby(['game_id'], as_index=False))

game_df = (game_df
           .assign(max_game_odd = game_id_group.transform(max),
                   min_game_odd = game_id_group.transform(min)))

game_df['favorite'] = np.where(game_df['min_game_odd'] get_ipython().getoutput("= game_df['max_game_odd'] and game_df['odds'] == game_df['min_game_odd'], 1, 0)")

















# Future variables
## Avg PF, PA, 
## Recent Performance: W, PF, PA
## Odds: Fav/Und buckets
## Fatigue - OT prior game

# Build Model








#chain example
game_df.groupby(['season_id','game_id'])['pts'].agg(['sum']).reset_index()









