
import pandas as pd
import re
from typing import Any

def load(df:pd.DataFrame)->pd.DataFrame:
    '''
    A function to read and load the streamlit dataframe into pandas dataframe.

    Args:
        - df: Whole dataframe [streamlit dataframe]

    Return:
        - df: a pandas dataframe
    '''
    df_name = df.name

    # check file type and read them accordingly
    if df_name[-3:] == 'csv':
        df = pd.read_csv(df, na_filter=False)
    else:
        df = pd.read_excel(df, na_filter=False)
    
    return df

def demography(df:pd.DataFrame)->list:
    '''
    A function to autoselect the demography columns. 

    Args:
        - df: Whole dataframe [pandas dataframe]

    Return:
        - default_demo: listof the column that contains string like 'age', 'gender', 'eth', 'income', 'urban'.
    '''
    default_demo = ['age', 'gender', 'eth', 'income', 'urban']
    data_list = list(df.columns)
    pattern = re.compile('|'.join(default_demo), re.IGNORECASE)
    default_demo = [item for item in data_list if pattern.search(item) and len(item.split()) <= 2]

    return default_demo

def col_search(df:pd.DataFrame, key:str)->list[str]:
    '''
    A function to autoselect column/s with the keyword.

    Args:
        - df: Whole dataframe [pandas dataframe]
        - key: keyword to match [str]

    Return:
        - columns_with_string: list of the column that contains certain keyword. 
    '''
    columns_with_string = []

    for column in df.columns:
        if key in column:
            columns_with_string.append(column)

    return columns_with_string


def sorter(demo:str, df:pd.DataFrame)->list[str]:
    '''
    A function to sort the list of the unique value in the demographic column.

    Args:
        - demo: Column name of the demography you're building the table on [str]
        - df: Whole dataframe [pandas dataframe]

    Return:
        - sorted list of unique values from specific column in the dataframe
    '''
    if re.search(r'age', demo, re.IGNORECASE):
        return sorted(list(df[demo].unique()))

    elif re.search(r'gender', demo, re.IGNORECASE):
        return sorted(list(df[demo].unique()),
                      key=lambda x: (re.match(r'^M|^L', x, re.IGNORECASE) is None,
                                     re.match(r'^F|^P', x, re.IGNORECASE) is None))

    elif re.search(r'eth', demo, re.IGNORECASE):
        return sorted(list(df[demo].unique()),
                      key=lambda x: (0 if re.match(r'^M', x, re.IGNORECASE) else
                                     1 if re.match(r'^C', x, re.IGNORECASE) else
                                     2 if re.match(r'^I', x, re.IGNORECASE) else
                                     3 if re.match(r'^B', x, re.IGNORECASE) else
                                     4 if re.match(r'^O|^L', x, re.IGNORECASE) else 5))

    elif re.search(r'income', demo, re.IGNORECASE):
        return sorted(list(df[demo].unique()))

    elif re.search(r'urban', demo, re.IGNORECASE):
        return sorted(list(df[demo].unique()),
                      key=lambda x: (0 if re.match(r'^U|^B', x) else
                                     1 if re.match(r'^S', x) else
                                     2 if re.match(r'^R|^L', x) else 3))
    
def sort_order(df:pd.DataFrame, sorting:list[str])->pd.DataFrame:
    '''
    A function to sort the order of crosstabs table based on the column selected by the user,

    Args:
        - df: Whole dataframe [pandas dataframe]
        - sorting: keyword to match [str]

    Return:
        - df: pandas dataframe that has been sorted either based on the `Grand Total` value or name. 
    '''
    if df.columns[0] in sorting:
        return df[:-1].sort_values(df.columns[0])
    else:
        return df[:-1].sort_values('Grand Total', ascending = False)

