import matplotlib.pyplot as plt
import numpy as np


def heatmap2d(arr: np.ndarray):
    plt.imshow(arr, cmap="viridis")
    plt.colorbar()
    plt.savefig("heatmap.png")
    plt.show()
