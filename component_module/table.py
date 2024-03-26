from io import BytesIO
from utils_module.processor import get_row, get_column
import pandas as pd

def write_table(
        df:pd.DataFrame, 
        demos:list[str], 
        wise:str, 
        q_ls:list[str], 
        multi:list[str], 
        name_sort:list[str], 
        weight:str,
        col_seqs:dict
        )->pd.DataFrame:
    
    '''
    Backend function to write the crosstabs table.
    This script serves as the top script for the back-end of the crosstabs generator.

    Args:
        - df: pandas DataFrame 
        - demos: List of name of the selected demography columns. 
        - wise: User selection of the value options. 
        - q_ls: List of question column. 
        - multi: List of column that contains multiple answer option.
        - name_sort: List of column to sort by the name. 
        - weight: Name of the selected weight column [str]
        - col_seqs:
            - Key: Demography column
            - Value: Sorted unique value of the key demography column.

    Return:
        - df_xlsx: pandas dataframe that contains crosstabs table.
    '''

    # Initialize excel file
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name= 'data')

    # Write tables one by one according to the type of question
    for demo in demos:
        if wise == 'Both':

            # start: loop counter to build the crosstabs table
            start = 1
            for q in q_ls:
                start, workbook, worksheet = get_column(
                    df=df, 
                    q=q, 
                    multi=multi, 
                    name_sort=name_sort, 
                    demo=demo, 
                    weight=weight, 
                    col_seqs=col_seqs, 
                    writer=writer, 
                    start=start
                    )

            # start_2: loop counter to build the crosstabs table
            start_2 = 1
            for q in q_ls:
                start_2, workbook, worksheet = get_row(
                    df=df, 
                    q=q, 
                    multi=multi, 
                    name_sort=name_sort, 
                    demo=demo, 
                    weight=weight, 
                    col_seqs=col_seqs, 
                    writer=writer, 
                    start_2=start_2
                    )

        elif wise == '% of Column Total':

            # start: loop counter to build the crosstabs table
            start = 1
            for q in q_ls:
                start, workbook, worksheet = get_column(
                    df=df, 
                    q=q, 
                    multi=multi, 
                    name_sort=name_sort, 
                    demo=demo, 
                    weight=weight, 
                    col_seqs=col_seqs, 
                    writer=writer, 
                    start=start
                    )

        else:
            # start_2: loop counter to build the crosstabs table
            start_2 = 1
            for q in q_ls:
                start_2, workbook, worksheet = get_row(
                    df=df, 
                    q=q, 
                    multi=multi, 
                    name_sort=name_sort, 
                    demo=demo, 
                    weight=weight, 
                    col_seqs=col_seqs, 
                    writer=writer, 
                    start_2=start_2
                    )
    writer.save()
    df_xlsx = output.getvalue()
    
    return df_xlsx