import matplotlib.pyplot as plt


def viz(df, save_dir, fontSize=14, title=""):
    info = []
    labels = df.columns.tolist()
    for i in range(df.shape[0]):
        avail = []
        data = df.loc[i]

        for j in range(1, len(data)):
            if data[j] == 1:
                avail.append(labels[j])

        info.append([data[0], "Chosen:\n" + "\n".join(avail)])

    fig, ax = plt.subplots(figsize=(10, 10))
    table = ax.table(info, loc="center")
    table.set_fontsize(fontSize)
    table.scale(1, 12)
    ax.axis("off")
    plt.title(title)

    fig.savefig(
        save_dir,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0,
    )
