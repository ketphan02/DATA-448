import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

colors = sns.color_palette("Set2")


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
    data = df.append(class_avg)
    colors[len(data) - 1] = "red"

    fig, ax = plt.subplots(figsize=(6.5, 6))
    plt.bar(height=data[field], x=data["Name"], color=colors)

    plt.title(name, fontsize=20)
    plt.ylabel(field, fontsize=16)
    plt.yticks(np.arange(0, max_num + 1).tolist())

    plt.show()
    fig.savefig(save_dir, dpi=300)
