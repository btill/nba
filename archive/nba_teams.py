
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import unicodedata

# NBA teams site
url = 'http://espn.go.com/nba/teams'

# Team site categories
team_categories = ('','stats','schedule','roster','depth',
	'transactions','ratings','photos','news','stadium')

def getTeamSiteSoup():
	r = requests.get(url)
	return BeautifulSoup(r.text)

def getTeamNames():
	soup = getTeamSiteSoup()
	team_tags = soup.find_all("div", class_="logo-nba-medium")
	teams = []
	for team_tag in team_tags:
		teams.append(team_tag.a.string)
	return teams

def getTeamUrls():
	soup = getTeamSiteSoup()
	team_tags = soup.find_all("div", class_="logo-nba-medium")
	team_names = getTeamNames()
	team_urls = dict.fromkeys(team_names)
	for team_tag in team_tags:
		team_urls[team_tag.a.string] = team_tag.a.get('href')
	return team_urls

def getTeamUrl(team_name, team_category=''):
	team_urls = getTeamUrls()
	if team_name not in team_urls.keys():
		return 'Invalid team name'
	elif (team_category not in team_categories) or (team_category == ''):
		return team_urls[team_name]
	else:
		a = team_urls[team_name].split('_')
		return a[0] + team_category + '/_' + a[1]

def getTeamRoster(team_name, convert_numerics=True, normalize_unicode=True):
	# get html from NBA team site
	url = getTeamUrl(team_name,'roster')
	r = requests.get(url)

	# pass html text to BeautifulSoup
	soup = BeautifulSoup(r.text)

	# Find player tags
	players = soup.find_all("tr", re.compile("player-"))

	# Roster columns
	roster_cols = ('Number','Name','Position','Age','Height',
		'Weight','College','Salary')
	roster_dict = {}
	for col in roster_cols: 
		roster_dict[col] = []

	# Construct dictionary of players
	for player in players:
		n = 0
		for col, n in zip(player.contents, range(len(player.contents))):
			raw_str = col.string
			if normalize_unicode:
				norm_str = unicodedata.normalize('NFKD', raw_str).encode('ascii','ignore')
			else:
				norm_str = raw_str
			roster_dict[roster_cols[n]].append(norm_str)

	roster = pd.DataFrame(roster_dict, columns=roster_cols)

	if convert_numerics:
		roster['Number'] = roster['Number'].astype('int64')
		roster['Age'] = roster['Age'].astype('int64')
		roster['Weight'] = roster['Weight'].astype('int64')
		roster['Height'] = getHeightInt(roster['Height'])
		roster['Salary'] = getSalaryInt(roster['Salary'])
		#roster.insert(5, 'Height (num)', getHeightInt(roster['Height']))
		#roster['Salary (num)'] = getSalaryInt(roster['Salary'])
		return roster
	else:
		return roster

def getHeightInt(height_strs):
	heights = []
	for h in height_strs:
		[feet, inches] = h.split('-')
		height_in = int(feet)*12 + int(inches)
		heights.append(height_in)
	return pd.Series(heights)

def getSalaryInt(salary_strs):
	salaries = []
	for s in salary_strs:
		if re.search('[$,]',s) == None:
			b = 0
		else:
			b = int(re.sub('[$,]','',s))
		salaries.append(b)
	return pd.Series(salaries)

#=============================================================================
# #Tests
# print getTeamNames()
# print getTeamUrls()
# print getTeamUrl('Golden State Warriors','stats')
# print getTeamUrl('Los Angeles Lakers','stadium')
# print getTeamRoster('Charlotte Bobcats')
# print getTeamRoster('Charlotte Bobcats','numerical')
# print getTeamRoster('Charlotte Bobcats','numerical').dtypes