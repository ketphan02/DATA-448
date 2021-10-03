import numpy as np
import matplotlib.pyplot as plt

def viz(df, class_avg, field, name, save_dir, max_num = 5):
    data = df.append(class_avg)
    colors = sns.color_palette("Set2")
    colors[len(data) - 1] = 'red'

    fig, ax = plt.subplots(figsize=(6.5, 6))
    plt.bar(height=data[field], x=data['Name'], color=colors)

    plt.title(name, fontsize=20)
    plt.ylabel(field, fontsize=16)
    plt.yticks(np.arange(0, max_num + 1).tolist())

    plt.show()
    fig.savefig(save_dir, dpi=300)