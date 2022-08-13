import re
import numpy as np
import pandas as pd
import datetime as dt
from datetime import date
import re
import sys

from teamPerformance import getTeamPerformance, getTeamSchedule, helperAaron

sys.path.insert(1, '')

from sportsipy.nba.teams import Teams
from sportsreference.nba.roster import Roster
from sportsreference.nba.roster import Player
from sportsreference.nba.schedule import Schedule
from sportsipy.nba.boxscore import Boxscore
from sportsipy.nba.boxscore import Boxscores


# filename = '../data/bettingOddsData/closing_betting_odds_2022_FIXED.csv'

def extract_lines(filename):
    startGameId = pd.read_csv(filename).head(1)['gameid'].iloc[0]
    endGameId = pd.read_csv(filename).tail(1)['gameid'].iloc[0]

    startDate = dt.datetime.strptime(startGameId[0:4] + ', ' + startGameId[4:6] + ', ' + startGameId[6:8], '%Y, %m, %d')
    endDate = dt.datetime.strptime(endGameId[0:4] + ', ' + endGameId[4:6] + ', ' + endGameId[6:8], '%Y, %m, %d')

    return startDate, endDate


def getRecentNGames(gameId, n, team):
    '''
    Obtains ids of the past n games (non inclusive) given the gameId of current game and team abbreviation
    
    '''
    if bool(re.match("^[\d]{9}[A-Z]{3}$", gameId)) == False:
        
        raise Exception('Issue with Game ID')

    
    if int(gameId[0:4]) == 2020: 
        if int(gameId[4:6].lstrip("0")) < 11: 
            teamSchedule = Schedule(team, int(gameId[0:4])).dataframe
        else:
            teamSchedule = Schedule(team, int(gameId[0:4]) + 1).dataframe
    else:
        if int(gameId[4:6].lstrip("0")) > 7: 
            teamSchedule = Schedule(team, int(gameId[0:4]) + 1).dataframe
        else:
            teamSchedule = Schedule(team, int(gameId[0:4])).dataframe

    teamSchedule.sort_values(by = 'datetime')
    currentDate = teamSchedule['datetime'].loc[gameId]
    temp = teamSchedule[(teamSchedule['datetime'] < currentDate)]

    if n > len(temp['datetime']):
        raise Exception('{} is too large'.format(n))

    gameIdList = list(temp['datetime'].tail(n).index)

    return gameIdList

def getTeamAveragePerformance(gameId, n, team):
    '''
    Returns a dataframe of average team performances in last n games
   
    '''
    #trying to only return the team stats of the team that we are asking for, rather than the team plus their opponents

    if int(gameId[0:4]) == 2020: 
        if int(gameId[4:6].lstrip("0")) < 11: 
            year = int(gameId[0:4])
        else:
            year = int(gameId[0:4]) + 1
    else:
        if int(gameId[4:6].lstrip("0")) > 7: 
            year = int(gameId[0:4]) + 1
        else:
            year = int(gameId[0:4])

    gameIdList = getRecentNGames(gameId, n, team)
    tempList = []

    df1, df2 = helperAaron(team, year)
    
    df1 = df1[df1.index.isin(gameIdList)]
    df2 = df2[df2.index.isin(gameIdList)]

    df = df1['home'].append(df2['away'])

    df.loc['mean'] = df.mean()

    df['teamAbbr'] = team
    
    return df.loc['mean']

def getPlayerAveragePerformance(gameId, n, playerId, team):
    '''
    Returns a dataframe of average player performances in last n games
   
    '''

    # WORK IN PROGRESS!!!!!!!!!!!!!!!!!!

    if int(gameId[0:4]) == 2020: 
        if int(gameId[4:6].lstrip("0")) < 11: 
            year = int(gameId[0:4])
        else:
            year = int(gameId[0:4]) + 1
    else:
        if int(gameId[4:6].lstrip("0")) > 7: 
            year = int(gameId[0:4]) + 1
        else:
            year = int(gameId[0:4])

    gameIdList = getRecentNGames(gameId, n, team)
    tempList = []

    fileLocation = 'data/gameStats/game_data_player_stats_{}.csv'.format(year)
    df = pd.read_csv(fileLocation, index_col = 0)


    gameIdList = getRecentNGames(gameId, n, team)
    playersAverageStats = [0] * 5
    playersAverageStats.append(playerId)

    for id in gameIdList:
        stats = getPlayerGameStatDataFrame(gameId)
        for x in range(0, 5):
            playersAverageStats[x] += float(stats.loc(playerId)[x])

    
    for y in range (1, 5):
        playersAverageStats[y] = round(float(playersAverageStats[y]/n), 3)


    return playersAverageStats


getTeamAveragePerformance('202003030DEN', 4, "DEN")
