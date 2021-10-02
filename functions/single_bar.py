import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

colors = sns.color_palette("Set2")

def viz(df, class_avg, field, name, save_dir, max_num = 5):
    data = df[field]
    team_avg = sum(data) / len(data)
    avg = class_avg[field]
    data = pd.DataFrame({
        'Name': ['Team average', 'Class average'],
        'Score': [team_avg, avg],
    })

    fig, ax = plt.subplots(figsize=(6.5, 6)) 

    ax = (
        sns
        .barplot(data=data, x='Name', y='Score')
        .set(xlabel='', ylabel=field, yticks=np.arange(0, max_num + 1).tolist())
    )
    
    plt.title(name, size=20)
    plt.ylabel(field, size=16)
    
    plt.show()
    fig.savefig(save_dir, dpi=300)