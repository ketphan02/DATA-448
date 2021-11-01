import cv2
import dataframe_image as dfi
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from IPython.display import display


def viz(csv_file, save_dir):
    df = pd.read_csv(csv_file, sep=";")
    df_display = df
    df_names = df["Name"].tolist()
    df_names.append("Total")
    df_rows = df.shape[0]
    df = df.drop(columns="Name")
    df.loc[df_rows] = df.sum()

    # Produce gridview
    fig = plt.figure(figsize=(20, 7))
    for i in range(len(df.columns.values)):
        ax = fig.add_subplot(2, len(df.columns.values) // 2, i + 1)
        plt.bar(height=[0, 4, 0],
                x=["foo", df.columns.values[i], "bar"],
                color="white")
        plt.bar(
            height=[0, df.loc[4].values[i], 0],
            x=["foo", df.columns.values[i], "bar"],
            color="#FF6B6B",
        )
        plt.yticks([0, 4])
        plt.xlim([df.columns.values[i], df.columns.values[i]])
        ax.spines["left"].set_color("black")
        ax.spines["top"].set_color("black")
        ax.spines["right"].set_color("black")
        ax.spines["bottom"].set_color("black")
        if i < len(df.columns.values) // 2:
            ax.xaxis.tick_top()
        plt.xticks([df.columns.values[i]], fontsize=15)
        plt.ylim((0, 4))
        plt.yticks([])

    plt.subplots_adjust(wspace=0, hspace=0)
    #     plt.show()
    fig.savefig("../../visualizations/section 2/temp/gridview.png", dpi=300)

    # Produce tally
    dfi.export(df_display, "../../visualizations/section 2/temp/dataframe.png")

    # Merge
    image1 = cv2.imread("../../visualizations/section 2/temp/gridview.png")
    image2 = cv2.imread("../../visualizations/section 2/temp/dataframe.png")
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
