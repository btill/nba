
import pandas as pd
import numpy as np

# load raw data
d = pd.read_csv('season1213.csv')
d = d.fillna(0)

# important categories
player_cats = ['Player','Pos','Age','Tm','G','GS','MP']
max_cats = ['PTS','3P','AST','STL','BLK','TRB']
pct_cats = ['FT%','FG%']
min_cats = ['TOV']
top_n = 12*9 # teams * starter

# initialize dz
dz = d[player_cats + max_cats + pct_cats + min_cats]
dz[max_cats + pct_cats + min_cats] = dz[max_cats + pct_cats + min_cats].astype('float')

def zTerms(df, cats):

	zdf = dict.fromkeys(cats)

	for cat in cats:
		d = df[cat][df[cat].notnull()]
		zdf[cat] = [d.mean(), d.std()]

	return zdf

def zScoreCats(df, zdf, invert=False):

	df_zscore = df

	for cat in zdf.keys():
		mu = zdf[cat][0]
		sigma = zdf[cat][1]
		df_zscore[cat] = (df_zscore[cat] - mu)/sigma
		if invert:
			df_zscore[cat] = -df_zscore[cat]

	return df_zscore

def zTotalAndRank(df, cats):

	df['Z'] = df[cats].apply(np.mean,axis=1)
	df = df.sort_index(by='Z', ascending=False)
	df = df.reset_index(drop=True)

	return df

# Score by max categories and rank
z = zTerms(dz, max_cats)
dz = zScoreCats(dz, z)
dz = zTotalAndRank(dz, max_cats)

# Re-score max and pct cats based on top 108 ranking
dz_top = dz.iloc[:top_n]
z = zTerms(dz_top, max_cats + pct_cats)
dz = zScoreCats(dz, z)

# Score min categories based on top 108 ranking
z = zTerms(dz_top, min_cats)
dz = zScoreCats(dz, z, invert=True)

# Perform final ranking
dz = zTotalAndRank(dz, max_cats+pct_cats+min_cats)

# Print and save
print dz.iloc[:3]
dz.to_csv('z_rankings.csv')
