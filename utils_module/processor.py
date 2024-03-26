from crosstab_module.crosstab import single_choice_crosstab_column, single_choice_crosstab_row
from crosstab_module.crosstab import multi_choice_crosstab_column, multi_choice_crosstab_row
import pandas as pd

def get_column(df:pd.DataFrame, q:str, multi:list[str], name_sort:list[str], demo:str, weight:str, col_seqs:list[list[str]], writer:pd.ExcelWriter, start:int)->tuple[int,pd.ExcelWriter,pd.ExcelWriter]:
    '''
    Generate the crosstab tables per column values using the multi_choice_crosstab_column function and single_choice_crosstab_column.

    Args:
        - df: Whole dataframe [pandas dataframe]
        - q: Column name of the question you're building the table on [str]
        - multi: Question that has multiple choice answer [str]
        - name_sort: list of the column to sort by name [str] 
        - demo: Item in the for loop function [str]
        - weight: Weight that you want to use to build the crosstab table [str]
        - col_seqs: Order of demographic sequence [list]
        - writer: Engine to write the Excel sheet
        - start: Number to loop [int]

    Return:
        - start: loop updated counter [int]
        - workbook: Excel workbook.
        - worksheet: Excel worksheet.
    '''
    if q in multi:
        table = multi_choice_crosstab_column(df=df, q=q, column=demo, value=weight, column_seq=col_seqs[demo])
    else:
        table = single_choice_crosstab_column(df=df, q=q, sorting=name_sort, column=demo, value=weight, column_seq=col_seqs[demo])

    table.to_excel(writer, index=False, sheet_name=f"{demo}(col)", startrow=start)
    start = start + len(table) + 3
    workbook = writer.book
    worksheet = writer.sheets[f"{demo}(col)"]
    
    return start, workbook, worksheet

def get_row(df:pd.DataFrame, q:str, multi:list[str], name_sort:list[str], demo:str, weight:str, col_seqs:list[list[str]], writer:pd.ExcelWriter, start_2:int)->tuple[int,pd.ExcelWriter,pd.ExcelWriter]:
    '''
    Generate the crosstab tables per row values using the multi_choice_crosstab_row function and single_choice_crosstab_row.

    Args:
        - df: Whole dataframe [pandas dataframe]
        - q: Column name of the question you're building the table on [str]
        - multi: Question that has multiple choice answer [str]
        - name_sort: list of the column to sort by name [str]
        - demo: Item in the for loop function [str]
        - weight: Weight that you want to use to build the crosstab table [str]
        - col_seqs: Order of demographic sequence [list]
        - writer: Engine to write the Excel sheet
        - start: Number to loop [int]

    Return:
        - start_2: loop updated counter [int]
        - workbook: Excel workbook.
        - worksheet: Excel worksheet.
    '''
    if q in multi:
        table_2 = multi_choice_crosstab_row(df=df, q=q, column=demo, value=weight, column_seq=col_seqs[demo])
    else:
        table_2 = single_choice_crosstab_row(df=df, q=q, sorting=name_sort, column=demo, value=weight, column_seq=col_seqs[demo])

    table_2.to_excel(writer, index=False, sheet_name=f"{demo}(row)", startrow=start_2)
    start_2 = start_2 + len(table_2) + 3
    workbook = writer.book
    worksheet = writer.sheets[f"{demo}(row)"]

    return start_2, workbook, worksheet