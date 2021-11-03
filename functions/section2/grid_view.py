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
        plt.xticks([df.columns.values[i]], fontsize=20)
        plt.ylim((0, 4))
        plt.yticks([])

    plt.subplots_adjust(wspace=0, hspace=0)
    #     plt.show()
    fig.savefig("../../visualizations/section 2/temp/gridview.png", dpi=300)

    # Produce tally
    info = []
    labels = df_display.columns.tolist()
    for i in range(df_display.shape[0]):
        avail = []
        data = df_display.loc[i]

        for j in range(1, len(data)):
            if data[j] == 1:
                avail.append(labels[j])

        info.append([data[0], "Choose:\n" + "\n".join(avail)])

    fig, ax = plt.subplots(figsize=(10, 10))
    table = ax.table(info, loc="center")
    table.set_fontsize(14)
    table.scale(1, 12)
    ax.axis("off")

    fig.savefig(
        "../../visualizations/section 2/temp/dataframe.png",
        dpi=300,
        bbox_inches="tight",
        pad_inches=0,
    )

    # Merge
    image1 = cv2.imread("../../visualizations/section 2/temp/gridview.png")
    image2 = cv2.imread("../../visualizations/section 2/temp/dataframe.png")
    image2 = cv2.copyMakeBorder(image2,
                                0,
                                50,
                                200,
                                200,
                                cv2.BORDER_CONSTANT,
                                value=[255, 255, 255])
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
