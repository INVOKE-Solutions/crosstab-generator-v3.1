
import pandas as pd
import re
from crosstab_module.crosstab import single_choice_crosstab_column, single_choice_crosstab_row
from crosstab_module.crosstab import multi_choice_crosstab_column, multi_choice_crosstab_row

def __init__(self):
    pass

def load(df):
    df_name = df.name

    # check file type and read them accordingly
    if df_name[-3:] == 'csv':
        df = pd.read_csv(df, na_filter=False)
    else:
        df = pd.read_excel(df, na_filter=False)
    
    return df

def demography(df):
    default_demo = ['age', 'gender', 'eth', 'income', 'urban']
    data_list = list(df.columns)
    pattern = re.compile('|'.join(default_demo), re.IGNORECASE)
    default_demo = [item for item in data_list if pattern.search(item) and len(item.split()) <= 2]

    return default_demo

def col_search(df, key):
    '''
    A function to autoselect column/s with the keyword.

    df: Whole dataframe [pandas dataframe]
    key: keyword to match [str]
    '''
    columns_with_string = []

    for column in df.columns:
        if key in column:
            columns_with_string.append(column)

    return columns_with_string


def sorter(demo, df):
    '''
    A function to sort the list of the unique value in the demographic column.

    demo: Column name of the demography you're building the table on [str]
    df: Whole dataframe [pandas dataframe]
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
    
def get_column(df, q, multi, demo, weight, col_seqs, writer, start):
    if q in multi:
        table = multi_choice_crosstab_column(df, q, demo, value=weight, column_seq=col_seqs[demo])
    else:
        table = single_choice_crosstab_column(df, q, demo, value=weight, column_seq=col_seqs[demo])

    table.to_excel(writer, index=False, sheet_name=f"{demo}(col)", startrow=start)
    start = start + len(table) + 3
    workbook = writer.book
    worksheet = writer.sheets[f"{demo}(col)"]
    
    return start, workbook, worksheet

def get_row(df, q, multi, demo, weight, col_seqs, writer, start_2):
    if q in multi:
        table_2 = multi_choice_crosstab_row(df, q, demo, value=weight, column_seq=col_seqs[demo])
    else:
        table_2 = single_choice_crosstab_row(df, q, demo, value=weight, column_seq=col_seqs[demo])

    table_2.to_excel(writer, index=False, sheet_name=f"{demo}(row)", startrow=start_2)
    start_2 = start_2 + len(table_2) + 3
    workbook = writer.book
    worksheet = writer.sheets[f"{demo}(row)"]

    return start_2, workbook, worksheet
