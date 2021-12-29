import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind
from scipy.stats import f_oneway

viz = {
    'grouped': [list(np.arange(1,17)), list(np.arange(17, 33))],
    'stacked': [list(np.arange(17,33)), list(np.arange(1,17))],
    'gridview': [list(np.arange(1,19)), list(np.arange(37,55)), list(np.arange(19,37))],
    'heatmap': [list(np.arange(19,37)), list(np.arange(1,19)), list(np.arange(37,55))],
    'tally': [list(np.arange(37,55)), list(np.arange(19,37)), list(np.arange(1,19))]
}

def get_viz_time(dfs, viz_type):
    """Gets average time per visualization for all the version"""
    versions = []
    data = viz[viz_type]
    length = 2 * len(data[0])
    for df in dfs:
        sm = 0
        for i in range(len(data)):
            if i < 2:
                df_t = df.iloc[i]
                for j in range(len(data[i])):
                    sm += float(df_t[f'Q{data[i][j]}_Page Submit'])
        versions.append(sm / length)
    return versions

def getVizAccuracy(dfs, section, vizType, ver):
    """for the given dataframe and visualization, gets the average accuracy for each version"""
    versions = []
    listOfQno = viz[vizType]
    # gets a df of all the choices made by the responders in the question variable
    j = 0
    for df in dfs:
        question = [col for i, col in enumerate(df.columns) if i > 17 and col.startswith('Q') and len(col.split()) == 1]
        question = df[question]
        correct = pd.read_csv(f'../report/answer/section {str(ver)}/{section+str(j+1)}.csv', delimiter= ";")
        accurayR1 = [question.loc[0][i-1] == correct.loc[0][i-1] for i in listOfQno[j]]
        accurayR2 = [question.loc[1][i-1] == correct.loc[0][i-1] for i in listOfQno[j]]
        r1 = pd.DataFrame(accurayR1)
        r2 = pd.DataFrame(accurayR2)
        numCorAnsR1 = r1[r1[0] == 1]
        numCorAnsR2 = r2[r2[0] == 1]
        perR1 = (len(numCorAnsR1)/len(correct.loc[0]))*100
        perR2 = (len(numCorAnsR2)/len(correct.loc[0]))*100
        avg = (perR1 + perR2)/2
        versions.append(avg)
        j+=1
    return versions

def t_test(df1, df2):
    """Culculates t-test between two average time and returns the p value"""
    time_1 = []
    time_2 = []
    for field in df1:
        if ('_Page Submit' in field):
            time_1 = time_1 + [df1[field][0], df1[field][1]]
    
    for field in df2:
        if ('_Page Submit' in field):
            time_2 = time_2 + [df2[field][0], df2[field][1]]

    a = np.array(time_1, dtype=float)
    b = np.array(time_2, dtype=float)
    return ttest_ind(a, b)[1]

def anova_test(dfs):
    time = []
    for df in dfs:
        temp = []
        for field in df:
            if ('_Page Submit' in field):
                temp = temp + [df[field][0], df[field][1]]
        time.append(np.array(temp, dtype=float))
    return f_oneway(*time)[1]

def clean_name(df):
    new_cols = df.columns.tolist()[:17]
    for i, val in enumerate(df.columns):
        if i < 17: continue

        if (len(val.split()) == 1):
            save = val
            new_cols.append(val)
        else:
            temp = val.split('_')
            temp[0] = save
            new_cols.append('_'.join(temp))

    name_change = {i:j for i,j in zip(df.columns,new_cols)}
    return df.rename(columns=name_change)

def get_correct_ans(df, answer_dir, id):

    # gets a df of all the choices made by the responders in the question variable
    question = [col for i, col in enumerate(df.columns) if i > 17 and col.startswith('Q') and len(col.split()) == 1]
    question = df[question]

    # imports the right answers
    correct = pd.read_csv(answer_dir, delimiter= ";")
    # takes first two responders from df and compare their choices with the correct answer
    accurayR1 = [question.loc[0][i] == correct.loc[0][i] for i in range(len(correct.loc[0]))]
    accurayR2 = [question.loc[1][i] == correct.loc[0][i] for i in range(len(correct.loc[0]))]


    r1 = pd.DataFrame(accurayR1)
    r2 = pd.DataFrame(accurayR2)
    numCorAnsR1 = r1[r1[0] == 1]
    numCorAnsR2 = r2[r2[0] == 1]
    perR1 = (len(numCorAnsR1)/len(correct.loc[0]))*100
    perR2 = (len(numCorAnsR2)/len(correct.loc[0]))*100
    avg = (perR1 + perR2)/2

    # put this into a variable 
    display(pd.DataFrame.from_dict({
        'Id': id,
        'Num. Questions': [len(correct.loc[0]), len(correct.loc[0])],
        'Correct Answer': [len(numCorAnsR1), len(numCorAnsR2)],
        'Accuracy': [f'{perR1:.2f}%', f'{perR2:.2f}%']
        }))
    return avg

def check_confused(dfs):
    plt.figure(figsize=(18,6))
    count = 0
    for df in dfs:
        question = [col for i, col in enumerate(df.columns) if i > 17 and col.startswith('Q') and len(col.split()) == 1]
        count = len(question)
        question = df[question]
        counts = [int(question[val][0] == "I can't tell from the graphs") + int(question[val][1] == "I can't tell from the graphs") for val in question]
        plt.plot(np.arange(1,len(counts)+1), counts)
    # Axis title need to be added
    plt.xlabel("Question Number")
    plt.xticks(np.arange(1, count, 1))
    plt.ylabel("""No. of time "I can't tell from graphs" was selected""")
    labels = ['Version ' + str(i+1) for i in range(len(dfs))]
    plt.legend(labels, loc='upper right')
    plt.show()

def time_display(df, title, res1, res2):
    data = [col for col in df.columns if 'Page Submit' in col]
    data = df[data]
    data1 = [float(val) for val in data.iloc[0].values.tolist()]
    plt.figure(figsize=(18,6))
    plt.plot(np.arange(1,(len(data1)+1)), data1)
    data2 = [float(val) for val in data.iloc[1].values.tolist()]
    plt.plot(np.arange(1,(len(data2)+1)), data2)
    plt.legend(['Responder ' + str(res1), 'Responder ' + str(res2)], loc='upper right')
    plt.title(title)
    plt.xticks(np.arange(1, len(data1)+1, 1))
    plt.xlabel("Question Number")
    plt.ylabel("Time taken to complete each question (in seconds)")
    plt.show()

def getAverageTime(df1,df2=pd.DataFrame(),df3=pd.DataFrame()):
    """Takes dataframe of each version and returns the average time per version"""
    listDf = [df1]
    ver = 1
    if df3.empty:
        listDf.append(df2)
    else:
        listDf.extend([df2,df3])
    # List of store dataframe for avg
    listOfDf = []
    for df in listDf:
        # create a own dataframe with just Duration column and added into a new df variable
        temp = df[['Duration (in seconds)']].astype(int)
        temp['Version'] = ver
        ver+=1
        temp = temp.reset_index()
        listOfDf.append(temp)
    merged_df = pd.concat(listOfDf,axis=0).reset_index()
    merged_df = merged_df.astype({"Version":str})
    merged_df['Id'] = ["Responder "+str(n[0]+1) for n in merged_df.iterrows()]
    display(merged_df[['Id','Duration (in seconds)', 'Version']])
    avg = merged_df.groupby(['Version']).mean()
    avg = avg.rename(columns= {'Duration (in seconds)': 'Average Duration (in seconds)'})
    display(avg[['Average Duration (in seconds)']])
    return [merged_df, avg]




        

    