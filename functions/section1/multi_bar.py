import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def viz(df, class_avg, field, name, save_dir, max_num=5):
    """
    Visualize n bars with n people of a particular field plus one bar for the class average.
    Parameters
    ----------
    df: pandas.DataFrame
        Dataframe containing the data.
    class_avg: pandas.DataFrame or dict
        Dataframe or dictionary containing the class averages of different fields.
    field: str
        The field to be visualized.
    name: str
        The title of the field.
    save_dir: str
        The directory to save the plot.
    max_num: int (default=5)
        The maximum length of y axis.
    """
    colors = sns.color_palette("Set2")
    data = df.append(class_avg)
    colors[len(data) - 1] = colors[-2]

    fig, ax = plt.subplots(figsize=(6.5, 6))
    h = ax.bar(height=data[field], x=data["Name"], color=colors)

    plt.title(name, fontsize=20)
    plt.xlabel(field, fontsize=16)
    plt.ylabel("Skill Level (Total)", fontsize=16)
    plt.yticks(np.arange(0, max_num + 1).tolist())
    ax.xaxis.set_ticklabels([])
    plt.legend(h,
               data["Name"],
               fontsize=14,
               bbox_to_anchor=(1.05, 1),
               loc=2,
               borderaxespad=0.0)

    plt.show()
    fig.savefig(save_dir, dpi=300, bbox_inches='tight')
