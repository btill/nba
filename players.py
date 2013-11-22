
import requests
from bs4 import BeautifulSoup
import re

def getSeasonStatSoup(year):

	# basketball-reference season stat page
	base_url = 'http://www.basketball-reference.com/leagues/NBA_%(year)d_totals.html'
	url = base_url % {'year': year}

	# BeautifulSoup parsing only works with "xml" parsing option -- not exactly sure why
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "xml")

	return soup

def getPlayerYear(name, year):

	soup = getSeasonStatSoup(year)

	# get category strings -- this assumes same order as stats
	cats = []
	cat_parent = soup.find('tr', class_='no_ranker thead')
	if cat_parent != None:
		cats_html = cat_parent.find_all('th')
		for cat in cats_html:
			cats.append(cat.get('data-stat'))

	# transform player name to "Last, First" format
	name_list = name.split(' ')
	name_list.reverse()
	csk_str = ','.join(name_list)

	# find player via csk_str, then iterate over stat entries
	stats = []
	tag = soup.find('td', csk=csk_str)
	if tag != None:
		stats_html = tag.parent.find_all('td')
		for stat in stats_html:
			# remove asterisk from some players
			stats.append(re.sub('\*','',stat.get_text())) 

	player_stats = dict(zip(cats, stats))
	return player_stats

def listPlayers(year):

	soup = getSeasonStatSoup(year)
	player_list = []
	tds = soup.find_all('td')
	for td in tds:
		txt = td.get_text()
		if td.has_attr('csk') and (re.search('\d', txt) == None) and (txt not in player_list):
			player_list.append(txt)
	return player_list








