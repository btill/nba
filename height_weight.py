
import nba_teams
import pandas as pd
import matplotlib.pyplot as plt
import nba_players

p = nba_players.getPlayers()
team_avgs = nba_players.getTeamAvgs()

plt.figure(1)
p.plot(x='Weight',y='Height',marker='.',linestyle='None')
plt.hold(True)
team_avgs.plot(x='Weight',y='Height',marker='o',linestyle='None')
plt.xlabel('Weight [lbs]')
plt.ylabel('Height [in]')

plt.figure(2)
p['Age'].hist(bins=len(range(p['Age'].min(), p['Age'].max())))
plt.show()
