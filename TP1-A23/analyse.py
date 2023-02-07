import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def plot_test_puissance():
    df = pd.read_csv('results.csv').groupby(['algo','size']).mean().reset_index()
    df['size'] = 2**df['size']
    df.to_csv('results_with_means.csv', index=False)
    g = sns.FacetGrid(df, hue='algo',  aspect=1)
    g = g.map(plt.plot, 'size', 'temps')
    g.set(xscale='log')
    g.set(yscale='log')
    g.add_legend()
    plt.savefig('test_puissance')
    plt.close()

def plot_test_rapport():
    df = pd.read_csv('results.csv').groupby(['algo','size']).mean().reset_index()
    df['size'] = 2**df['size']
    df['rapport'] = df['temps']/df['size']**3
    g2 = sns.lineplot(df, x="size", y="rapport", hue='algo')
    for algo in df['algo'].unique():
        last_point = df[df['algo']==algo].tail(1)['rapport'].values[0]
        print(f"Rapport = {last_point} pour l'algorithme {algo}")
    plt.savefig('test_rapport')
    plt.close()

def plot_test_constante():
    df = pd.read_csv('results.csv').groupby(['algo','size']).mean().reset_index()
    df['size'] = 2**df['size']
    df['Fn'] = df['size']**3
    for algo in df['algo'].unique():
        slope, intercept, r_value, p_value, std_err = stats.linregress(df[df['algo']==algo]['Fn'],df[df['algo']==algo]['temps'])
        print(f"Temps = {slope} * Fn + {intercept} pour l'algorithme {algo}")
    g2 = sns.lineplot(df, x="Fn", y="temps", hue='algo')
    plt.savefig('test_constante')
    plt.close()

plot_test_puissance()
plot_test_rapport()
plot_test_constante()
