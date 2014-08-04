
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle
import re
import matplotlib.pyplot as plt

def getShootingChartHTML(name, year):

	prefix_url = 'http://www.basketball-reference.com/players/'
	suffix_url = '/shooting/' + str(year) + '/'

	name_sep = name.lower().split(' ')
	first_name = name_sep[0]
	last_name = name_sep[1]
	name_url = first_name[0] + '/' + last_name[:5] + first_name[:2] + '01'

	url = prefix_url + name_url + suffix_url

	r = requests.get(url)
	return r.text


def getShootingData(name, year, save_html=False):

	# scrape HTML and save in file (in this same folder as this file)
	shooting_html = getShootingChartHTML(name, year)
	shooting_html = re.sub('<br>',' ',shooting_html) # get rid of <br> tags (hack so BS4 works)

	# save html for debugging
	if save_html:
		f = open(name + '_' + str(year) + '_shooting_chart.html', 'w')
		pickle.dump(shooting_html, f)
		f.close()

	# soupify
	soup = BeautifulSoup(shooting_html, "xml")

	# all shot information is contained in a single div with id 'shot-wrapper'
	shots = soup.find_all('div', id='shot-wrapper')

	# pixel position (x, y)
	divs = shots[0].find_all('div',style=True)
	xpx = []
	ypx = []
	for div in divs:
		raw_str = re.findall('position:absolute;top:-?\d+px;left:-?\d+px', div['style'])
		if len(raw_str) > 0:
			coord_str = re.findall('-?\d+', raw_str[0])
			y = float(coord_str[0])
			x = float(coord_str[1])
			ypx.append(float(coord_str[0])) # y is first coordinate, and starts from top
			xpx.append(float(coord_str[1])) # x is second coordinate, and starts from left

	# distance, shot type (pts), and make/miss
	spans = shots[0].find_all('span',tip=True)
	dist = []
	pts = []
	made = []
	for span in spans:
		dist_str = re.findall('\d+ ft',span['tip'])
		if len(dist_str) > 0:
			dist_iso = dist_str[0].split(' ft')
			dist.append(int(dist_iso[0]))

		pts_str = re.findall('\d-pointer', span['tip'])
		if len(pts_str) > 0:
			pts_iso = pts_str[0].split('-pointer')
			pts.append(int(pts_iso[0]))

		made.append('Made' in span['tip'])

	# package
	shot_dict = {'Xpx': xpx, 'Ypx': ypx, 'Dist': dist, 'Pts': pts, 'Made': made}
	shots = pd.DataFrame(shot_dict)
	return shots

#====================================================================
name = 'Blake Griffin'
year = 2014

shots = getShootingData(name, year)

total_pts = shots[shots['Made']==True]['Pts'].sum()
num_shots = len(shots.index)
print 'pts/shot = ', float(total_pts)/float(num_shots)

plt.figure(1)
plt.plot(shots[shots['Made']==False].Xpx, shots[shots['Made']==False].Ypx, marker='x', linestyle='None')
plt.plot(shots[shots['Made']==True].Xpx, shots[shots['Made']==True].Ypx, marker='o', linestyle='None')
plt.axis('scaled')
plt.axis([0, 500, 0, 350])
plt.title(name + ' - ' + str(year))
plt.show()
