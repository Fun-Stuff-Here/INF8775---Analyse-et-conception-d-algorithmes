import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# df = pd.read_csv('results.csv').groupby(['algo','size']).mean().reset_index()
# g = sns.FacetGrid(df, hue='algo', size=4, aspect=1)
# g = g.map(plt.plot, 'size', 'temps')
# g.set(xscale='log')
# g.set(yscale='log')
# g.add_legend()
# plt.savefig('test_puissance')


df = pd.read_csv('results.csv').groupby(['algo','size']).mean().reset_index()
df['rapport'] = df['temps']/df['size']**3
g2 = sns.lineplot(df, x="size", y="rapport", hue='algo', size=4, aspect=1)
g2.add_legend()
plt.savefig('test_rapport')
