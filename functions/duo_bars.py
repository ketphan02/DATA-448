import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

colors = sns.color_palette("Set2")


def viz(df, class_avg, name, save_dir, max_len=15):
    '''
    Visualize class average versus team average by duobars.

    Parameters
    ----------
    df : pandas.DataFrame
            DataFrame containing the data.
    class_avg : pandas.DataFrame
            A dataframe that contain all average of all fields.
    name : str
            Title of the plot.
    save_dir : str
            Directory to save the visualizaton.
    max_len : int (default=15)
            Maximum length of the y axis.
    '''

    data = df.drop(columns='Name')
    labels = data.columns
    data = sum(data.values)
    class_avg = class_avg.drop(columns='Name').values[0].tolist()

    space = 1
    each_col_width = 3
    n = len(data)
    # graph_length = each_col_width * 2 * n + space * (n  + 1)

    bar_loc = [((i + 1) * space) + (i * 2 * each_col_width) +
               each_col_width for i in range(n)]
    x_left = [x - each_col_width / 2 for x in bar_loc]
    x_right = [x + each_col_width / 2 for x in bar_loc]

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.bar(height=data, x=x_left,
           color=colors[0], align='center', width=each_col_width)
    ax.bar(height=class_avg, x=x_right,
           color=colors[1], align='center', width=each_col_width)

    plt.xticks(bar_loc)
    ax.set_xticklabels(labels, fontsize=14)
    plt.yticks(np.arange(0, max_len + 1).tolist())
    plt.title(name, fontsize=20)
    plt.legend(['Team Average', 'Class average'], fontsize=12)

    plt.show()
    fig.savefig(save_dir, dpi=300)
