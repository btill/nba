
import requests
from bs4 import BeautifulSoup
import re
# import unittest
# import sys

base_url = 'http://www.basketball-reference.com/leagues/NBA_%(year)d_totals.html'

def getPlayerStats(name, year):

	# basketball-reference player stats
	url = base_url % {'year': year}

	# pass raw html to BeautifulSoup
	# only works with "xml" parsing option -- not exactly sure why
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "xml")

	# csk string formatting; used to find player in html
	name_list = name.split(' ')
	name_list.reverse()
	csk_str = ','.join(name_list)

	# find player via csk_str, then parse parent tree for stats
	stats = []
	tag = soup.find('td', csk=csk_str)
	if tag != None:
		stats_html = tag.parent.find_all('td')
		for stat in stats_html:
			stats.append(re.sub('\*','',stat.get_text())) # remove asterisk from some players

	# get category strings
	cats = []
	cat_parent = soup.find('tr', class_='no_ranker thead')
	if cat_parent != None:
		cats_html = cat_parent.find_all('th')
		for cat in cats_html:
			cats.append(cat.get('data-stat'))

	# combine into player_stats dictionary
	player_stats = dict(zip(cats, stats))

	return player_stats

# # unittest
# class TestPlayerStats(unittest.TestCase):

# 	def setUp(self):
# 		self.cases = [('Klay Thompson', 2013), ('Kobe Bryant', 2002), ('Michael Jordan', 1996), ('Player', 2013), ('Anthony Davis', 2000)]
# 		self.expected_success = [True, True, True, False, False]

# 	def test_getPlayerStats(self):
# 		for n, case in enumerate(self.cases):
# 			result = getPlayerStats(case[0], case[1])
# 			self.assertEqual(len(result) > 0, self.expected_success[n])

# if __name__ == '__main__':
#     unittest.main()

# # print getPlayerStats('Klay Thompson', 2013))
# # print getPlayerStats('Kobe Bryant', 2002)
# # print getPlayerStats('Michael Jordan', 1996)
# # print getPlayerStats('Player X', 2013)
# # print getPlayerStats('Anthony Davis', 2000)
