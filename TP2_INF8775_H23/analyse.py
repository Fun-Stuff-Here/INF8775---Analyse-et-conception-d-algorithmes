import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np

def plot_test_puissance():
    df = pd.read_csv('results.csv').groupby(['algo','size']).mean().reset_index()
    df.to_csv('results_with_means.csv', index=False)
    g = sns.FacetGrid(df, hue='algo',  aspect=1)
    for algo in df['algo'].unique():
        slope, intercept, r_value, p_value, std_err = stats.linregress( np.log(df[df['algo']==algo]['size']),np.log(df[df['algo']==algo]['temps']))
        # print(f"Temps = {slope} * Fn + {intercept} pour l'algorithme {algo}")
    g = g.map(plt.plot, 'size', 'temps')
    g.set(xscale='log')
    g.set(yscale='log')
    g.add_legend()
    plt.savefig('test_puissance')
    plt.close()

# def plot_test_rapport():
#     df = pd.read_csv('results.csv').groupby(['algo','size']).mean().reset_index()
#     df['size'] = 2**df['size']
#     for algo in df['algo'].unique():
#         data = df.filter(df[df['algo'] ==algo])
#         if algo == 'conv':
#             data['rapport'] = data['temps']/data['size']**3
#         elif algo == 'strassen':
#             data['rapport'] = data['temps']/data['size']**2.807
#         elif algo == 'strassenSeuil':
#             data['rapport'] = data['temps']/data['size']**2.75
#         else : 
#             raise ValueError(f"Algorithme {algo} inconnu")
#         sns.lineplot(data, x="size", y="rapport")
#         plt.savefig(f"test_rapport_{algo}")
#         plt.close()

# def plot_test_constante():
#     df = pd.read_csv('results.csv').groupby(['algo','size']).mean().reset_index()
#     df['size'] = 2**df['size']
#     for algo in df['algo'].unique():
#         data = df.filter(df[df['algo'] ==algo])
#         if algo == 'conv':
#             data['Fn'] = data['size']**3
#         elif algo == 'strassen':
#             data['Fn'] = data['size']**2.807
#         elif algo == 'strassenSeuil':
#             data['Fn'] = data['size']**2.75
#         else : 
#             raise ValueError(f"Algorithme {algo} inconnu")
#         slope, intercept, r_value, p_value, std_err = stats.linregress(data['Fn'],data['temps'])
#         print(f"Temps = {slope} * Fn + {intercept} pour l'algorithme {algo}")
#         sns.lineplot(data, x="Fn", y="temps")
#         plt.savefig(f"test_constante_{algo}")
#         plt.close()

plot_test_puissance()
# plot_test_rapport()
# plot_test_constante()
