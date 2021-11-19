import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

colors = sns.color_palette("Set2")


def viz(df, class_avg, name, save_dir, max_len=5) -> None:
    w = 4
    g = 2

    legend_labels = df["Name"].tolist()
    legend_labels.append("Class average")
    data = df.drop(columns="Name")
    labels = data.columns

    bars_loc = [g * (i + 1) + i * (4 * w) + 2 * w for i in range(len(labels))]

    pos_s = []

    for anchor in bars_loc:
        x1 = anchor - w
        x2 = anchor
        x3 = anchor + w
        x4 = anchor + 2 * w
        pos_s.append([x1, x2, x3, x4])

    fig, ax = plt.subplots(figsize=(9, 6))
    data.loc[len(data)] = class_avg.drop(columns="Name").values[0].tolist()
    values = data.values.T
    colors[len(data) - 1] = colors[-2]

    for i, pos in enumerate(pos_s):
        h = ax.bar(x=pos,
                   height=values[i],
                   width=w,
                   align="center",
                   color=colors)

    bars_loc = [x + w // 2 for x in bars_loc]
    # plt.legend(h, legend_labels, fontsize=14)
    plt.xticks(bars_loc)
    plt.title(name, fontsize=20)
    plt.ylabel("Skill Level (Total)", fontsize=16)
    ax.set_xticklabels(labels, fontsize=16)
    plt.yticks(np.arange(0, max_len + 1).tolist())
    plt.legend(h, legend_labels, fontsize=14,
               bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()

    fig.savefig(save_dir, dpi=300)
