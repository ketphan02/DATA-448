import cv2
import matplotlib.pyplot as plt
import pandas as pd

from functions.section2 import tally


def viz(csv_file, title, save_dir, need_tally=False):
    df = pd.read_csv(csv_file, sep=";")
    df_display = df
    num_ppl = df.shape[0]
    df_names = df["Name"].tolist()
    df_names.append("Total")
    df_rows = df.shape[0]
    df = df.drop(columns="Name")
    df.loc[df_rows] = df.sum()

    # Produce gridview
    fig = plt.figure(figsize=(20, 7))
    for i in range(len(df.columns.values)):
        ax = fig.add_subplot(2, len(df.columns.values) // 2, i + 1)
        plt.bar(
            height=[0, num_ppl, 0],
            x=["foo", df.columns.values[i], "bar"],
            color="white",
        )
        plt.bar(
            height=[0, df.loc[num_ppl].values[i], 0],
            x=["foo", df.columns.values[i], "bar"],
            color="#FF6B6B",
        )
        plt.yticks([0, num_ppl])
        plt.xlim([df.columns.values[i], df.columns.values[i]])
        ax.spines["left"].set_color("black")
        ax.spines["top"].set_color("black")
        ax.spines["right"].set_color("black")
        ax.spines["bottom"].set_color("black")
        if i < len(df.columns.values) // 2:
            ax.xaxis.tick_top()
        plt.xticks([df.columns.values[i]], fontsize=20)
        plt.ylim((0, num_ppl))
        plt.yticks([])

    fig.suptitle(title, fontsize=50)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)

    if need_tally:
        fig.savefig("../../visualizations/section 2/temp/gridview.png",
                    dpi=300)

        # Produce tally
        tally.viz(df_display,
                  "../../visualizations/section 2/temp/dataframe.png")

        # Merge
        image1 = cv2.imread("../../visualizations/section 2/temp/gridview.png")
        image2 = cv2.imread(
            "../../visualizations/section 2/temp/dataframe.png")
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
        fig.savefig(save_dir, dpi=300)
