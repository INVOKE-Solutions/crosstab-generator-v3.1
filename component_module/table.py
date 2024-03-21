
from io import BytesIO
from utils_module.processor import get_row, get_column
from chart_module.chart import load_chart, crosstab_reader
import pandas as pd

def write_table(
        df:pd.DataFrame, 
        demos:list[str], 
        wise:str, 
        q_ls:list[str], 
        multi:list[str], 
        name_sort:list[str], 
        weight:str,
        col_seqs:dict,
        )->pd.DataFrame:
    
    # Initialize excel file
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name= 'data')

    # Write tables one by one according to the type of question
    for demo in demos:
        if wise == 'Both':
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