import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

colors = sns.color_palette("Set2")


def viz(df, class_avg, field, name, save_dir, max_num=5):
    """
    Visualize two bar graphs (choosen field and class average of that field).

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
    data = df[field]
    team_avg = sum(data) / len(data)
    avg = class_avg[field]
    data = pd.DataFrame(
        {
            "Name": ["Team average", "Class average"],
            "Score": [team_avg, avg],
        }
    )

    fig, ax = plt.subplots(figsize=(6.5, 6))

    sns.barplot(data=data, x="Name", y="Score").set(
        yticks=np.arange(0, max_num + 1).tolist()
    )

    plt.title(name, size=20)
    plt.xlabel(field, size=16)
    plt.ylabel("Score", size=16)

    plt.show()
    fig.savefig(save_dir, dpi=300)
