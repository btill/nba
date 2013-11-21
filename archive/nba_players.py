
import nba_teams
import pandas as pd

players_csv = 'players/players.csv'
team_avgs_csv = 'teams/team_avgs.csv'

def updatePlayersCSV():
	teams = nba_teams.getTeamNames()
	r_master_init = False
	for team in teams:
		r = nba_teams.getTeamRoster(team)
		r.insert(8, 'Team', [team]*len(r.index))
		if not r_master_init:
			r_master = r
			r_master_init = True
		else:
			r_master = pd.concat([r_master, r], ignore_index=True)
		print team + " complete"
	r_master.to_csv(players_csv, index=False)

def updateTeamAvgsCSV():
	p = getPlayers()
	teams = nba_teams.getTeamNames()
	avg_cols = ['Age','Height','Weight','Salary']
	team_avgs = pd.DataFrame(index=teams, columns=avg_cols)
	for team in teams:
		team_stats = p[p['Team'] == team]
		team_avg = team_stats.mean().ix[avg_cols]
		team_avgs.ix[team] = team_avg.values
	 	print team + " complete"
	team_avgs = team_avgs.astype('float')
	team_avgs.to_csv(team_avgs_csv)

def getPlayers():
	return pd.read_csv(players_csv)

def getTeamAvgs():
	return pd.read_csv(team_avgs_csv,index_col=0)

def findPlayers(val, category='Name'):
	p = getPlayers()
	return p[p[category]==val]

def rankPlayers(category, top=True, n=10):
	p = getPlayers()
	return p.sort(category, ascending=not top).irow(range(n))

def sortTeamAvgs(category, top=True, n=10):
	team_avgs = getTeamAvgs()
	return team_avgs.sort(category, ascending=not top).irow(range(n))

# # ===== Test =====
# print sortTeamAvgs('Salary', top=True, n=3)
# print rankPlayers('Age', top=False, n=10)
# print findPlayers('Anthony Davis')
# print findPlayers('Arizona State','College')