import cv2
import dataframe_image as dfi
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import seaborn as sns

def make_colormap():
#     colors = ["#76EAD7", "#4CD3C2","#2FC4B2", "#12947F"] # blue
    colors = ["#FCD2D1", "#FE8F8F", "#FF5C58", "#F54748"] # red
    return mcolors.LinearSegmentedColormap.from_list("", colors)
    

def viz(csv_file, save_dir):
    df = pd.read_csv(csv_file, sep=";")
    df_display = df
    df = df.drop(labels="Name", axis=1)
    df.loc['No. of members']= df.sum(axis=0)
    df = df.drop(labels=[0,1,2,3], axis=0)

    # Produce gridview
    ax, fig = plt.subplots(figsize=(8,3))
    ax = sns.heatmap(df, cmap=make_colormap(), yticklabels = False)
    ax.collections[0].colorbar.set_ticks([0.0, 1.0, 2.0, 3.0, 4.0])
    ax.set_xticklabels(
        ax.get_xticklabels(), 
        rotation=50, 
        horizontalalignment = 'right'
    )
    plt.tight_layout()
    plt.savefig("../../visualizations/section 2/temp/heatmap.png", dpi=300)

    # Produce tally
    dfi.export(df_display, "../../visualizations/section 2/temp/dataframe_1.png")

    # Merge
    image1 = cv2.imread("../../visualizations/section 2/temp/heatmap.png")
    image2 = cv2.imread("../../visualizations/section 2/temp/dataframe_1.png")
    ratio = image1.shape[1] / image2.shape[1]
    size = (int(image1.shape[1] / ratio), int(image1.shape[0] / ratio))
    image1 = cv2.resize(image1, size, cv2.INTER_NEAREST)
    image = cv2.vconcat([image1, image2])
    image = cv2.copyMakeBorder(image,
                               0,
                               20,
                               0,
                               0,
                               cv2.BORDER_CONSTANT,
                               None,
                               value=[255, 255, 255])
    cv2.imwrite(save_dir, image)