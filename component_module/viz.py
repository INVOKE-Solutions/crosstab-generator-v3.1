from io import BytesIO
import xlsxwriter
import pandas as pd
from chart_module.chart import crosstab_reader

def draw_chart(dfs:list[pd.DataFrame], sheet_names:list):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    # Process each table separately
    for sheet_idx, (sheet_name, df) in enumerate(zip(sheet_names, dfs)):
        workbook, charts = crosstab_reader(workbook, df, sheet_name)
            
    workbook.close()
    df_charts = output.getvalue()
    return df_charts
    