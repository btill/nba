
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
	f = open('shooting_chart.txt', 'w')
	pickle.dump(r.text, f)
	f.close()

getShootingChartHTML('Brandon Jennings', 2013)

f = open('shooting_chart.txt','r')
soup = BeautifulSoup(f.read())
f.close()

shots = soup.find_all('div', id='shot-wrapper')

divs = shots[0].find_all('div')
xpx = []
ypx = []
for div in divs:
	raw_str = re.findall('position:absolute;top:\d+px;left:\d+px',div['style'])
	if len(raw_str) > 0:
		coord_str = re.findall('\d+', raw_str[0])
		ypx.append(int(coord_str[0]))
		xpx.append(int(coord_str[1]))

spans = shots[0].find_all('span')
dist = []
pts = []
made = []
for span in spans:
	dist_str = re.findall('\d+ ft',span['tip'])
	dist_iso = dist_str[0].split(' ft')
	dist.append(int(dist_iso[0]))

	pts_str = re.findall('\d-pointer', span['tip'])
	pts_iso = pts_str[0].split('-pointer')
	pts.append(int(pts_iso[0]))

	made.append('Made' in span['tip'])

shot_dict = {'Xpx': xpx, 'Ypx': ypx, 'Dist': dist, 'Pts': pts, 'Made': made}

print len(xpx), len(dist)

shots = pd.DataFrame(shot_dict)

total_pts = shots[shots['Made']==True]['Pts'].sum()
num_shots = len(shots.index)
print float(total_pts)/float(num_shots)

plt.figure(1)
shots[shots['Made']==False].plot(x='Xpx',y='Ypx',marker='x',linestyle='None',markerfacecolor='r')
plt.hold(True)
shots[shots['Made']==True].plot(x='Xpx',y='Ypx',marker='o',linestyle='None',markerfacecolor='b')
plt.show()
