import streamlit as st
import pandas as pd
import datetime as dt
import math
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
from PIL import Image
import matplotlib.pyplot as plt
from colour import Color
import numpy as np
import re

# Hide streamlit header and footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)


def single_choice_crosstab_column(df, q, column=None, value='weight', column_seq=None, row_seq=None):
    '''
    Create a table for single choice questions (column wise).

    df: Whole dataframe [pandas dataframe]
    q: Column name of the question you're building the table on [str]
    column: Column name of the demographic column that you're building the table across, would only generate the grand total when undefined [str]
    value: Column name of your weights [str]
    column_seq: Order of demographic sequence [list]
    row_seq: Order of answer sequence [list]
    '''

    if row_seq != None:
        row_list = row_seq + ["Grand Total"]
    else:
        # .value_counts() to sort the column in descending order
        row_list = list(dict(df[q].value_counts()).keys()) + ["Grand Total"]
    # dict.keys() to return the column names in the dictionary
    row_labels = list(filter(None, row_list))
    # list to put the column names in a list
    # create a data frame with q as the header
    df_ct = pd.DataFrame({q: row_labels})

    if column_seq != None:
        column_seq = column_seq + ['Grand Total']
    else:
        # .unique to find the unique elements in the array
        column_seq = list(df[column].unique()) + ['Grand Total']

    for demo in column_seq:
        temp = []
        for row in df_ct[q]:
            if row != 'Grand Total':
                if demo != 'Grand Total':
                    # to find the total weight of demo
                    new_df = df[df[column] == demo]
                    updated_df = new_df[q].replace('', np.nan)
                    back_df = updated_df.dropna()
                    weight_list = df[value].to_list()
                    total_sum = 0
                    for j in back_df.index:
                        sum = weight_list[j]
                        total_sum += sum
                    # to create dataFrame of demo == row
                    temp_df = df[(df[column] == demo) & (df[q] == row)]
                    if total_sum == 0:
                        temp.append(0)
                    else:
                        # divide conditional weight (demo == row) over total weight (demo)
                        temp.append(round(temp_df[value].sum()/total_sum, 4))
                else:
                    updated_df = df[q].replace('', np.nan)
                    back_df = updated_df.dropna()
                    weight_list = df[value].to_list()
                    total_sum = 0
                    for j in back_df.index:
                        sum = weight_list[j]
                        total_sum += sum
                    temp_df = df[df[q] == row]
                    # divide conditional weight (row) over total weight (overall)
                    temp.append(round(temp_df[value].sum()/total_sum, 4))
            else:
                # to find the total weight of demo
                new_df = df[df[column] == demo]
                updated_df = new_df[q].replace('', np.nan)
                back_df = updated_df.dropna()
                if (back_df.empty == False) or (demo == 'Grand Total'):
                    temp.append(1)
                else:
                    temp.append(0)

        # Add new column to the data frame and input the values
        df_ct[demo] = temp

    if row_seq == None:
        df_ct = pd.concat(
            [df_ct[:-1].sort_values('Grand Total', ascending=False), df_ct[-1:]])
    return df_ct


def single_choice_crosstab_row(df, q, column=None, value='weight', column_seq=None, row_seq=None):
    '''
    Create a table for single choice questions (row wise).

    df: Whole dataframe [pandas dataframe]
    q: Column name of the question you're building the table on [str]
    column: Column name of the demographic column that you're building the table across, would only generate the grand total when undefined [str]
    value: Column name of your weights [str]
    column_seq: Order of demographic sequence [list]
    row_seq: Order of answer sequence [list]
    '''
    if row_seq != None:
        row_list = row_seq + ["Grand Total"]
    else:
        # .value_counts() to sort the column in descending order
        row_list = list(dict(df[q].value_counts()).keys())
    # dic.keys() to return the column names in the dictionary
    row_labels = list(filter(None, row_list))
    # list to put the column names in a list
    # create a data frame with q as the header
    df_ct = pd.DataFrame({q: row_labels})

    if column_seq != None:
        column_seq = column_seq + ['Grand Total']
    else:
        # .unique to find the unique elements in the array
        column_seq = list(df[column].unique()) + ['Grand Total']

    for demo in column_seq:
        temp = []
        for row in df_ct[q]:
            if demo != 'Grand Total':
                # to find the total weight of question
                total_sum = df[df[q] == row][value].sum()
                # to create dataFrame of demo == row
                temp_df = df[(df[column] == demo) & (df[q] == row)]
                # divide conditional weight (demo == row) over total weight (question)
                temp.append(round(temp_df[value].sum()/total_sum, 4))
            else:
                temp.append(1)

        # Add new column to the data frame and input the values
        df_ct[demo] = temp

    return df_ct


def multi_choice_crosstab_column(df, q, column, value='weight', column_seq=None):
    '''
    Create a table for multi choice questions (column wise).

    df: Whole dataframe [pandas dataframe]
    q: Column name of the question you're building the table on [str]
    column: Column name of the demographic column that you're building the table across, would only generate the grand total when undefined [str]
    value: Column name of your weights [str]
    column_seq: Order of demographic sequence [list]
    row_seq: Order of answer sequence [list]
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
            # create a dataframe of all rows that contain demo
            demo_df = df[df[column] == demo]

        updated_df = demo_df[q].replace('', np.nan)
        temp_df = updated_df.dropna()
        weight_list = df[value].to_list()
        total_sum = 0
        for j in temp_df.index:
            sum = weight_list[j]
            total_sum += sum

        for i in temp_df.index:
            # extract all answers of question q with index i in the form of a string
            answer = str(demo_df[q][i])
            if answer != 'nan':
                answer = answer.split(', ')  # split the answers
                for ans in answer:
                    if ans not in ans_dict:
                        # create an input in the ans_dict with its weight
                        ans_dict[ans] = df[value][i]
                    else:
                        # add the weight of the same input in the ans_dict
                        ans_dict[ans] += df[value][i]

        for key, val in ans_dict.items():
            # divide each input with the total weight sum of demo
            ans_dict[key] = round(val/total_sum, 4)
        # sort the items in descending order
        ans_dict = dict(
            sorted(ans_dict.items(), key=lambda x: x[1], reverse=True))
        if demo == 'Grand Total':
            row_list = list(ans_dict.keys())
            row_labels = list(filter(None, row_list))
            gt = list(ans_dict.values())
        else:
            # create a dictionary of demo and its items + values
            demo_dict[demo] = ans_dict
    # create a column of the question and the row labels
    result = pd.DataFrame({q: row_labels})
    for demo in demo_dict:
        temp = []
        for row in row_labels:
            if row in demo_dict[demo]:
                # append demo/row value in the demo_dict
                temp.append(demo_dict[demo][row])
            else:
                temp.append(0.0000)
        # add new column of demo and temp in the result dataframe
        result[demo] = temp
    result['Grand Total'] = gt
    return result


def multi_choice_crosstab_row(df, q, column, value='weight', column_seq=None):
    '''
    Create a table for multi choice questions (row wise).

    df: Whole dataframe [pandas dataframe]
    q: Column name of the question you're building the table on [str]
    column: Column name of the demographic column that you're building the table across, would only generate the grand total when undefined [str]
    value: Column name of your weights [str]
    column_seq: Order of demographic sequence [list]
    row_seq: Order of answer sequence [list]
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
        # extract all answers of question q with index i in the form of a string
        answer = str(df[q][i])
        if answer != 'nan':
            answer = answer.split(', ')  # split the answers
            for ans in answer:
                if ans not in ans_dict:
                    # create an input in the ans_dict with its weight
                    ans_dict[ans] = df[value][i]
                else:
                    # add the weight of the same input in the ans_dict
                    ans_dict[ans] += df[value][i]

    for demo in column_seq:
        ans_dict2 = {}
        if demo == 'Grand Total':
            demo_df = df
        else:
            # create a dataframe of all rows that contain demo
            demo_df = df[df[column] == demo]

        updated_df2 = demo_df[q].replace('', np.nan)
        temp_df2 = updated_df2.dropna()

        for i in temp_df2.index:
            # extract all answers of question q with index i in the form of a string
            answer = str(demo_df[q][i])
            if answer != 'nan':
                answer = answer.split(', ')  # split the answers
                for ans in answer:
                    if ans not in ans_dict2:
                        # create an input in the ans_dict with its weight
                        ans_dict2[ans] = df[value][i]
                    else:
                        # add the weight of the same input in the ans_dict
                        ans_dict2[ans] += df[value][i]

        new_dict = {x: float(ans_dict2[x])/ans_dict[x] for x in ans_dict2}
        new_dict = {key: round(new_dict[key], 4) for key in new_dict}
        # sort the items in descending order
        new_dict = dict(
            sorted(new_dict.items(), key=lambda x: x[1], reverse=True))

        if demo == 'Grand Total':
            row_labels = list(new_dict.keys())
            gt = list(new_dict.values())
        else:
            # create a dictionary of demo and its items + values
            demo_dict[demo] = new_dict

    # create a column of the question and the row labels
    result = pd.DataFrame({q: row_labels})
    for demo in demo_dict:
        temp = []
        for row in row_labels:
            if row in demo_dict[demo]:
                # append demo/row value in the demo_dict
                temp.append(demo_dict[demo][row])
            else:
                temp.append(0.0000)
        # add new column of demo and temp in the result dataframe
        result[demo] = temp
    result['Grand Total'] = gt
    return result


def sorter(demo, df):
    '''
    Create a function to sort the list of the unique value in the demographic column.

    demo: Column name of the demography you're building the table on [str]
    df: Whole dataframe [pandas dataframe]
    '''
    if demo == 'agegroup':
        return sorted(list(df['agegroup'].unique()))

    elif demo == 'gender':
        return sorted(list(df['gender'].unique()),
                      key=lambda x: (re.match(r'^M|^L', x, re.IGNORECASE) is None,
                                     re.match(r'^F|^P', x, re.IGNORECASE) is None))

    elif demo == 'ethgroup':
        return sorted(list(df['ethgroup'].unique()),
                      key=lambda x: (0 if re.match(r'^M', x, re.IGNORECASE) else
                                     1 if re.match(r'^C', x, re.IGNORECASE) else
                                     2 if re.match(r'^I', x, re.IGNORECASE) else
                                     3 if re.match(r'^B', x, re.IGNORECASE) else
                                     4 if re.match(r'^O|^L', x, re.IGNORECASE) else 5))

    elif demo == 'incomegroup':
        return sorted(list(df['incomegroup'].unique()))

    elif demo == 'urbanity':
        return sorted(list(df['urbanity'].unique()),
                      key=lambda x: (0 if re.match(r'^U|^B', x) else
                                     1 if re.match(r'^S', x) else
                                     2 if re.match(r'^R|^L', x) else 3))


def multi_column(df, key):
    '''
    Create a function to autoselect the multiple answer column.

    df: Whole dataframe [pandas dataframe]
    key: keyword [str]
    '''
    columns_with_string = []

    for column in df.columns:
        if key in column:
            columns_with_string.append(column)

    return columns_with_string


image = Image.open('invoke_logo.jpg')
st.title('Crosstabs Generator')
st.image(image)

st.subheader("Upload Survey responses (csv/xlsx)")
df = st.file_uploader(
    "Please ensure the data are cleaned and weighted (if need to be) prior to uploading.")
if df:
    df_name = df.name
    # check file type and read them accordingly
    if df_name[-3:] == 'csv':
        df = pd.read_csv(df, na_filter=False)
    else:
        df = pd.read_excel(df, na_filter=False)

    # weight_columns = [col for col in df.columns if 'weight' in col.lower()]
    weight = st.multiselect('Select weight column and choose only 1',
                            ['', 'weight', 'untrimmed_weight', 'trimmed_weight', 'Unweighted'], ['untrimmed_weight', 'trimmed_weight'])
    if weight != '':
        default_demo = ['agegroup', 'gender',
                        'ethgroup', 'incomegroup', 'urbanity']
        data_list = list(df.columns)
        default_demo = [item for item in default_demo if item in data_list]
        demos = st.multiselect(
            'Choose the demograhic(s) you want to build the crosstabs across', list(
                df.columns) + default_demo, default_demo)

        if len(demos) > 0:
            # Ensure that all the demographic values have been selected before proceeding
            score = 0
            col_seqs = {}
            for demo in demos:
                st.subheader('Column: ' + demo)
                col_seq = st.multiselect(
                    'Please arrange ALL values in order', list(
                        df[demo].unique()),
                    default=sorter(demo, df=df), key=demo)
                col_seqs[demo] = col_seq
                if len(col_seq) == df[demo].nunique():
                    score += 1

            if score == len(demos):
                first = st.selectbox('Select the first question of the survey',
                                     [''] + list(df.columns))
                if first != '':
                    first_idx = list(df.columns).index(first)
                    last = st.selectbox('Select the last question of the survey', [
                                        ''] + list(df.columns)[first_idx + 1:])
                    if last != '':
                        last_idx = list(df.columns).index(last)
                        st.subheader(
                            'Number of questions to build the crosstab on: ' + str(last_idx - first_idx + 1))
                        q_ls = [df.columns[x]
                                for x in range(first_idx, last_idx + 1)]
                        wise_list = ['% of Column Total',
                                     '% of Row Total', 'Both']
                        wise = st.selectbox(
                            'Show values as:', [''] + wise_list)
                        if wise != '':
                            multi = st.multiselect('Choose mutiple answers question(s), if any', list(
                                df.columns)[first_idx: last_idx + 1], multi_column(df[first_idx: last_idx + 1],
                                                                                   key="[MULTI]"))
                            button = st.button('Generate Crosstabs')
                            if button:
                                with st.spinner('Building crosstabs...'):
                                    # Initialize excel file
                                    output = BytesIO()
                                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                                    df.to_excel(writer, index=False, sheet_name= 'data')

                                    # Write tables one by one according to the type of question
                                    for demo in demos:
                                        if wise == 'Both':
                                            start = 1
                                            for q in q_ls:
                                                if q in multi:
                                                    table = multi_choice_crosstab_column(df, q, demo, value= weight, column_seq= col_seqs[demo])
                                                else:
                                                    table = single_choice_crosstab_column(df, q, demo, value= weight, column_seq= col_seqs[demo])

                                                table.to_excel(writer, index=False, sheet_name=f"{demo}(column)", startrow = start)
                                                start = start + len(table) + 3
                                                workbook = writer.book
                                                worksheet = writer.sheets[f"{demo}(column)"]

                                            start_2 = 1
                                            for q in q_ls:
                                                if q in multi:
                                                    table_2 = multi_choice_crosstab_row(df, q, demo, value= weight, column_seq= col_seqs[demo])
                                                else:
                                                    table_2 = single_choice_crosstab_row(df, q, demo, value= weight, column_seq= col_seqs[demo])

                                                table_2.to_excel(writer, index=False, sheet_name=f"{demo}(row)", startrow = start_2)
                                                start_2 = start_2 + len(table_2) + 3
                                                workbook = writer.book
                                                worksheet = writer.sheets[f"{demo}(row)"]
                                        
                                        elif wise == '% of Column Total':
                                            start = 1
                                            for q in q_ls:
                                                if q in multi:
                                                    table = multi_choice_crosstab_column(df, q, demo, value= weight, column_seq= col_seqs[demo])
                                                else:
                                                    table = single_choice_crosstab_column(df, q, demo, value= weight, column_seq= col_seqs[demo])

                                                table.to_excel(writer, index=False, sheet_name=f"{demo}(column)", startrow = start)
                                                start = start + len(table) + 3
                                                workbook = writer.book
                                                worksheet = writer.sheets[f"{demo}(column)"]

                                        else:
                                            start = 1
                                            for q in q_ls:
                                                if q in multi:
                                                    table = multi_choice_crosstab_row(df, q, demo, value= weight, column_seq= col_seqs[demo])
                                                else:
                                                    table = single_choice_crosstab_row(df, q, demo, value= weight, column_seq= col_seqs[demo])

                                                table.to_excel(writer, index=False, sheet_name=f"{demo}(row)", startrow = start)
                                                start = start + len(table) + 3
                                                workbook = writer.book
                                                worksheet = writer.sheets[f"{demo}(row)"]
                                
                                writer.save()
                                df_xlsx = output.getvalue()
                                df_name = df_name[:df_name.find('.')]
                                st.balloons()
                                st.header('Crosstabs ready for download!')
                                st.download_button(label='📥 Download', data=df_xlsx, file_name= df_name + '-crosstabs.xlsx')
