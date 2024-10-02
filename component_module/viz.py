from io import BytesIO
import xlsxwriter
import pandas as pd
from chart_module.chart import crosstab_reader

def draw_chart(dfs: list[pd.DataFrame], sheet_names: list) -> bytes:
    '''
    Backend function to draw the clustered column chart.
    This script serves as the top script for the back-end of the chart generator.

    Args:
        - dfs: list of pandas DataFrame 
        - sheet_names: list of the sheet names in the crosstabs file. 

    Return:
        - df_charts: crosstabs table that contains clustered column chart.
    '''
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    # Process each table separately
    for _, (sheet_name, df) in enumerate(zip(sheet_names, dfs)):
        workbook, _ = crosstab_reader(workbook, df, sheet_name)
    
    workbook.close()
    
    df_charts = output.getvalue()
    
    return df_charts
    