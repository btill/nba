
import nba_teams
import pandas as pd

def calcBMI(roster): 
	weights = roster['Weight'].astype('float')
	heights = roster['Height'].astype('float')
	BMI = weights/(heights**2)*703.0 # see wikipedia
	return BMI

def calcBodyFatPct(roster):
	BMI = calcBMI(roster)
	ages = roster['Age'].astype('float')
	bodyFatPct = 1.20*BMI + 0.23*ages - 10.80 - 5.40 # see wikipedia
	return bodyFatPct

def getHealthStats(roster):
	r = roster[['Name','Age','Height','Weight']]
	r['BMI'] = calcBMI(roster)
	r['BF%'] = calcBodyFatPct(roster)
	return r

# Write health stats to CSVs for all teams
teams = nba_teams.getTeamNames()
#teams = ['Los Angeles Lakers','Golden State Warriors']
for team in teams:
	r = nba_teams.getTeamRoster(team,convert_numerics=True)
	bs = getHealthStats(r)
	bs.to_csv("health_stats/" + team + ".csv")
	print team + " complete"

