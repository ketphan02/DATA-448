import pandas as pd

def preprocessing(fileName, label=[0,1]):
    """Gets the csv into a DataFrame and removes the unnecessary rows"""
    df = pd.read_csv(fileName)
    df = df.drop(labels=label, axis=0)
    return df