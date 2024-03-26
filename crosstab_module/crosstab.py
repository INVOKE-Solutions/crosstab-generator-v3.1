import pandas as pd
import numpy as np
from utils_module.utils import sort_order

def single_choice_crosstab_column(
        df:pd.DataFrame, 
        q:str, 
        sorting:list[str], 
        column:str=None, 
        value:int='weight', 
        column_seq:list[str]=None, 
        row_seq:list[str]=None
        )->pd.DataFrame:
    '''
    Create a table for single choice questions (column wise).
    This script serves as the base script for the back-end of the crosstabs generator.

    Args:
        - df: Whole dataframe [pandas dataframe]
        - q: Column name of the question you're building the table on [str]
        - column: Column name of the demographic column that you're building the table across, would only generate the grand total when undefined [str]
        - value: Column name of your weights [str]
        - column_seq: Order of demographic sequence [list]
        - row_seq: Order of answer sequence [list]

    Return:
        - df_ct: pandas dataframe with crosstabs table. 
    '''

    if row_seq != None:
        row_list = row_seq + ["Grand Total"]
    else:
        row_list = list(dict(df[q].value_counts()).keys()) + ["Grand Total"] # .value_counts() to sort the column in descending order
    row_labels = list(filter(None, row_list))                                # dict.keys() to return the column names in the dictionary
                                                                             # list to put the column names in a list
    df_ct = pd.DataFrame({q: row_labels})                                    # create a data frame with q as the header

    if column_seq != None:
        column_seq = column_seq + ['Grand Total']
    else:
        column_seq = list(df[column].unique()) + ['Grand Total'] # .unique to find the unique elements in the array

    for demo in column_seq:
        temp = []
        for row in df_ct[q]:
            if row != 'Grand Total':
                if demo != 'Grand Total':
                    new_df = df[df[column] == demo] # to find the total weight of demo
                    updated_df = new_df[q].replace('', np.nan)
                    back_df = updated_df.dropna()
                    weight_list = df[value].to_list()
                    total_sum = 0
                    for j in back_df.index:
                        sum = weight_list[j]
                        total_sum += sum
                    temp_df = df[(df[column] == demo) & (df[q] == row)] # to create dataFrame of demo == row
                    if total_sum == 0:
                        temp.append(0)
                    else:
                        temp.append(round(temp_df[value].sum()/total_sum, 4)) # divide conditional weight (demo == row) over total weight (demo)
                else:
                    updated_df = df[q].replace('', np.nan)
                    back_df = updated_df.dropna()
                    weight_list = df[value].to_list()
                    total_sum = 0
                    for j in back_df.index:
                        sum = weight_list[j]
                        total_sum += sum
                    temp_df = df[df[q] == row]
                    temp.append(round(temp_df[value].sum()/total_sum, 4)) # divide conditional weight (row) over total weight (overall)
            else:
                new_df = df[df[column] == demo] # to find the total weight of demo
                updated_df = new_df[q].replace('', np.nan)
                back_df = updated_df.dropna()
                if (back_df.empty == False) or (demo == 'Grand Total'):
                    temp.append(1)
                else:
                    temp.append(0)

        df_ct[demo] = temp # Add new column to the data frame and input the values

    if row_seq == None:
        df_ct = pd.concat([sort_order(df=df_ct, sorting=sorting), df_ct[-1:]])
    return df_ct


def single_choice_crosstab_row(
        df:pd.DataFrame, 
        q:str, 
        sorting:list[str], 
        column:str=None, 
        value:int='weight', 
        column_seq:list[str]=None, 
        row_seq:list[str]=None
        )->pd.DataFrame:
    '''
    Create a table for single choice questions (row wise).
    This script serves as the base script for the back-end of the crosstabs generator.

    Args:
        - df: Whole dataframe [pandas dataframe]
        - q: Column name of the question you're building the table on [str]
        - column: Column name of the demographic column that you're building the table across, would only generate the grand total when undefined [str]
        - value: Column name of your weights [str]
        - column_seq: Order of demographic sequence [list]
        - row_seq: Order of answer sequence [list]

    Return:
        - df_ct: pandas dataframe with crosstabs table.
    '''
    if row_seq != None:
        row_list = row_seq + ["Grand Total"]
    else:
        row_list = list(dict(df[q].value_counts()).keys()) # .value_counts() to sort the column in descending order
    row_labels = list(filter(None, row_list))              # dic.keys() to return the column names in the dictionary
                                                           # list to put the column names in a list
    df_ct = pd.DataFrame({q: row_labels})                  # create a data frame with q as the header

    if column_seq != None:
        column_seq = column_seq + ['Grand Total']
    else:
        column_seq = list(df[column].unique()) + ['Grand Total'] # .unique to find the unique elements in the array

    for demo in column_seq:
        temp = []
        for row in df_ct[q]:
            if demo != 'Grand Total':
                total_sum = df[df[q] == row][value].sum() # to find the total weight of question
                temp_df = df[(df[column] == demo) & (df[q] == row)] # to create dataFrame of demo == row
                temp.append(round(temp_df[value].sum()/total_sum, 4)) # divide conditional weight (demo == row) over total weight (question)
            else:
                temp.append(1)

        df_ct[demo] = temp # Add new column to the data frame and input the values

    if row_seq == None:
        df_ct = pd.concat([sort_order(df=df_ct, sorting=sorting), df_ct[-1:]])
    return df_ct


def multi_choice_crosstab_column(
        df:pd.DataFrame, 
        q:str, 
        column:str, 
        value:int='weight', 
        column_seq:list[str]=None
        )->pd.DataFrame:
    '''
    Create a table for multi choice questions (column wise).
    This script serves as the base script for the back-end of the crosstabs generator.

    Args:
        - df: Whole dataframe [pandas dataframe]
        - q: Column name of the question you're building the table on [str]
        - column: Column name of the demographic column that you're building the table across, would only generate the grand total when undefined [str]
        - value: Column name of your weights [str]
        - column_seq: Order of demographic sequence [list]
        - row_seq: Order of answer sequence [list]

    Return:
        - result: pandas dataframe with crosstabs table.
    '''

    if column_seq != None:
        column_seq = column_seq + ['Grand Total']
    else:
        column_seq = list(df[column].unique())
        column_seq.sort()
        column_seq = column_seq + ['Grand Total']

    demo_dict = {}
    for demo in column_seq:
        ans_dict = {}
        if demo == 'Grand Total':
            demo_df = df
        else:
            demo_df = df[df[column] == demo] # create a dataframe of all rows that contain demo

        updated_df = demo_df[q].replace('', np.nan)
        temp_df = updated_df.dropna()
        weight_list = df[value].to_list()
        total_sum = 0
        for j in temp_df.index:
            sum = weight_list[j]
            total_sum += sum

        for i in temp_df.index:
            answer = str(demo_df[q][i]) # extract all answers of question q with index i in the form of a string
            if answer != 'nan':
                answer = answer.split(', ')  # split the answers
                for ans in answer:
                    if ans not in ans_dict:
                        ans_dict[ans] = df[value][i] # create an input in the ans_dict with its weight
                    else:
                        ans_dict[ans] += df[value][i] # add the weight of the same input in the ans_dict

        for key, val in ans_dict.items():
            ans_dict[key] = round(val/total_sum, 4) # divide each input with the total weight sum of demo
        ans_dict = dict(sorted(ans_dict.items(), key=lambda x: x[1], reverse=True)) # sort the items in descending order
        if demo == 'Grand Total':
            row_list = list(ans_dict.keys())
            row_labels = list(filter(None, row_list))
            gt = list(ans_dict.values())
        else:
            demo_dict[demo] = ans_dict # create a dictionary of demo and its items + values
    result = pd.DataFrame({q: row_labels}) # create a column of the question and the row labels
    for demo in demo_dict:
        temp = []
        for row in row_labels:
            if row in demo_dict[demo]:
                temp.append(demo_dict[demo][row]) # append demo/row value in the demo_dict
            else:
                temp.append(0.0000)
        result[demo] = temp # add new column of demo and temp in the result dataframe
    result['Grand Total'] = gt
    return result


def multi_choice_crosstab_row(
        df:pd.DataFrame, 
        q:str, 
        column:str, 
        value:int='weight', 
        column_seq:list[str]=None
        )->pd.DataFrame:
    '''
    Create a table for multi choice questions (row wise).
    This script serves as the base script for the back-end of the crosstabs generator.

    Args:
        - df: Whole dataframe [pandas dataframe]
        - q: Column name of the question you're building the table on [str]
        - column: Column name of the demographic column that you're building the table across, would only generate the grand total when undefined [str]
        - value: Column name of your weights [str]
        - column_seq: Order of demographic sequence [list]
        - row_seq: Order of answer sequence [list]

    Return:
        - result: pandas dataframe with crosstabs table.
    '''

    if column_seq != None:
        column_seq = column_seq + ['Grand Total']
    else:
        column_seq = list(df[column].unique())
        column_seq.sort()
        column_seq = column_seq + ['Grand Total']

    demo_dict = {}
    ans_dict = {}

    updated_df = df[q].replace('', np.nan)
    temp_df = updated_df.dropna()

    for i in temp_df.index:
        answer = str(df[q][i]) # extract all answers of question q with index i in the form of a string
        if answer != 'nan':
            answer = answer.split(', ')  # split the answers
            for ans in answer:
                if ans not in ans_dict:
                    ans_dict[ans] = df[value][i] # create an input in the ans_dict with its weight
                else:
                    ans_dict[ans] += df[value][i] # add the weight of the same input in the ans_dict

    for demo in column_seq:
        ans_dict2 = {}
        if demo == 'Grand Total':
            demo_df = df
        else:
            demo_df = df[df[column] == demo] # create a dataframe of all rows that contain demo

        updated_df2 = demo_df[q].replace('', np.nan)
        temp_df2 = updated_df2.dropna()

        for i in temp_df2.index:
            answer = str(demo_df[q][i]) # extract all answers of question q with index i in the form of a string
            if answer != 'nan':
                answer = answer.split(', ')  # split the answers
                for ans in answer:
                    if ans not in ans_dict2:
                        ans_dict2[ans] = df[value][i] # create an input in the ans_dict with its weight
                    else:
                        ans_dict2[ans] += df[value][i] # add the weight of the same input in the ans_dict

        new_dict = {x: float(ans_dict2[x])/ans_dict[x] for x in ans_dict2}
        new_dict = {key: round(new_dict[key], 4) for key in new_dict}
        new_dict = dict(sorted(new_dict.items(), key=lambda x: x[1], reverse=True)) # sort the items in descending order

        if demo == 'Grand Total':
            row_labels = list(new_dict.keys())
            gt = list(new_dict.values())
        else:
            demo_dict[demo] = new_dict # create a dictionary of demo and its items + values

    result = pd.DataFrame({q: row_labels}) # create a column of the question and the row labels
    for demo in demo_dict:
        temp = []
        for row in row_labels:
            if row in demo_dict[demo]:
                temp.append(demo_dict[demo][row]) # append demo/row value in the demo_dict
            else:
                temp.append(0.0000)
        result[demo] = temp # add new column of demo and temp in the result dataframe
    result['Grand Total'] = gt
    return result