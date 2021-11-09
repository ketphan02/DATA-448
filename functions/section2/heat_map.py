import cv2
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

from functions.section2 import tally


def make_colormap():
    #     colors = ["#76EAD7", "#4CD3C2","#2FC4B2", "#12947F"] # blue
    colors = ["#FFFFFF", "#FFB344", "#F54748"]  # red
    return mcolors.LinearSegmentedColormap.from_list("", colors)


def viz(csv_file, title, save_dir, need_tally=False):
    df = pd.read_csv(csv_file, sep=";")
    df_display = df
    num_user = df.shape[0]
    df = df.drop(labels="Name", axis=1)
    df.loc["No. of members"] = df.sum(axis=0)
    df = df.drop(labels=np.arange(0, num_user, 1), axis=0)

    # Produce gridview
    ax, fig = plt.subplots(figsize=(9, 4.5))
    ax = sns.heatmap(df, cmap=make_colormap(),
                     yticklabels=False, vmin=0, vmax=num_user)
    ax.collections[0].colorbar.set_ticks(np.arange(0, num_user + 1, 1))
    ax.set_xticklabels(ax.get_xticklabels(),
                       rotation=50,
                       horizontalalignment="right")
    plt.title(title, fontsize=25, y=1.1)
    plt.tight_layout()

    if need_tally:
        plt.savefig("../../visualizations/section 2/temp/heatmap.png", dpi=300)

        # Produce tally
        tally.viz(df_display, '../../visualizations/section 2/temp/dataframe_1.png')

        # Merge
        image1 = cv2.imread("../../visualizations/section 2/temp/heatmap.png")
        image2 = cv2.imread(
            "../../visualizations/section 2/temp/dataframe_1.png")
        image2 = cv2.copyMakeBorder(image2,
                                    0,
                                    0,
                                    100,
                                    100,
                                    cv2.BORDER_CONSTANT,
                                    value=[255, 255, 255])
        ratio = image1.shape[1] / image2.shape[1]
        size = (int(image1.shape[1] / ratio), int(image1.shape[0] / ratio))
        image1 = cv2.resize(image1, size, cv2.INTER_NEAREST)
        image = cv2.vconcat([image1, image2])
        cv2.imwrite(save_dir, image)
    else:
        plt.savefig(save_dir, dpi=300)
