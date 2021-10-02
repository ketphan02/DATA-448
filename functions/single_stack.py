import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

colors = sns.color_palette("Set2")


def viz(df, class_avg, field, name, save_dir, max_num=15):
    data = df[field]
    sums = sum(data)
    avg = class_avg[field]
    labels = list(df["Name"])[::-1]
    labels.insert(0, "Average")

    fig, ax = plt.subplots(figsize=(6.5, 6))
    ax.plot(
        ["foo", field, "bar"], [avg * 3] * 3, linestyle="--", color="red", linewidth=3
    )
    for i in range(len(data) - 1, -1, -1):
        ax.bar(height=[0, sums, 0], x=["foo", field, "bar"], color=colors[i], width=1)
        sums -= data[i]

    ax.xaxis.set_visible(False)
    plt.legend(labels, fontsize=14)
    plt.ylabel(field, size=16)
    plt.yticks(np.arange(0, max_num + 1).tolist())
    plt.title(name, size=20)

    sns.despine()

    plt.show()
    fig.savefig(save_dir, dpi=300)
