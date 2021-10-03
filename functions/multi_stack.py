import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

colors = sns.color_palette("Set2")

def viz(df, name, save_dir, max_len = 15) -> None:
    '''
	Visualize multiple stacked plot.

	Parameters:
	----------
	df: pandas.DataFrame
		Dataframe to be visualized.
	name: str
		Title of the plot.
	save_dir: str
		Directory to save the visualization.
	max_len: int
		Maximum length of the y axis.
    '''

    # Clean data for graph x labels
    fields = df.columns[1:].tolist()
    fields.insert(0, '')
    fields.append('')
    
    # Clean data for graph legend
    data = team_a
    labels = list(data["Name"])
    labels.insert(0, "Average")
    data = data.drop(columns='Name')
    
    # padding for the graph x axis
    avg = class_avg.drop(columns='Name').iloc[[0]].values[0].tolist()
    avg.insert(0, 0)
    avg.append(0)
    
    # padding for the graph y axis
    data.loc[len(data)] = 0
    data.loc[-1] = 0
    data.index = data.index + 1
    data = data.sort_index()
    
    # visualize
    fig, ax = plt.subplots(figsize=(9, 6))

    avg_lw = 1 / (len(fields) - 1)
    sums = sum(data.values).tolist()

    for i in range(1, len(fields) - 1):
        width = i * avg_lw
        if i > 1:
            ax.axhline(
                y=avg[i],
                xmax= width + (avg_lw / 2), xmin= width - (avg_lw / 2),
                linewidth=3,
                linestyle='--',
                color='red',
                label='_nolegend_'
            )
        else:
            ax.axhline(
                y=avg[i],
                xmax= width + (avg_lw / 2), xmin= width - (avg_lw / 2),
                linewidth=3,
                linestyle='--',
                color='red',
            )

        ax.bar(height=sums, x=np.arange(avg_lw, 1 - avg_lw, avg_lw), width=0.15, color=colors[i - 1])
        sums = sums - data.iloc[[i]].values[0]

    ax.set_xticks(np.arange(0, 1 + avg_lw, avg_lw).tolist())
    plt.yticks(np.arange(0, max_len + 1).tolist())
    ax.set_xticklabels(fields, fontsize=14)
    ax.set_title(name, fontsize=20)
    plt.legend(labels)
    plt.show()
    fig.savefig(save_dir, dpi=300)