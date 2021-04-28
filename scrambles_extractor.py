import pandas as pd

# DL https://www.worldcubeassociation.org/results/misc/export.html

df = pd.read_csv('WCA_export_Scrambles.tsv', delimiter='\t')

df = df[df['eventId'].isin(['222', 'pyram', 'skewb'])]
df = df[['scramble', 'eventId']]
df.scramble = df.scramble.str.split(' u| r| l| b').str[0]
df = df.drop_duplicates()
df = df.reset_index(drop=True)

df.to_csv("WCA_scrambles_clean.csv")
