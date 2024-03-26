from skimage.measure import label, regionprops
import pandas as pd
import numpy as np
from typing import Any

def load_chart(df_charts:pd.DataFrame)->tuple[list[pd.DataFrame],list,str]:
    '''
    A function to read and load the streamlit dataframe into pandas dataframe.
    
    Args:
        - df_charts: Whole dataframe [streamlit dataframe]
    
    Return:
        - dfs: List of pandas dataframe.
        - sheet_names: Name of the sheet
        - df_chartsname: Name of the uploaded file
    '''
    df_chartsname = df_charts.name
    # Read all sheet names in the Excel file
    all_sheet_names = pd.ExcelFile(df_charts).sheet_names

    # Exclude the first sheet (raw data)
    sheet_names_to_read = all_sheet_names[1:]

    # Rename sheets based on initial sheet names
    sheet_names = [name for name in sheet_names_to_read]

    # Read all tables from multiple sheets
    dfs = []
    for sheet_name in sheet_names_to_read:
        df = pd.read_excel(df_charts, sheet_name=sheet_name, header=None)
        dfs.append(df)
    
    return dfs, sheet_names, df_chartsname

def generate_bar_chart(df:pd.DataFrame, start:int, workbook:pd.ExcelWriter, worksheet:pd.ExcelWriter)->Any:
    '''
    Generate the clustered bar chart based on the crosstab table.
    This script serves as the base script for the back-end of the chart generator.

    Args:
        - df: Whole dataframe [pandas dataframe]
        - start: Row's number to start the loop [int]
        - workbook: Excel workbook [pandas ExcelWriter]
        - worksheet: Sheet in the Excel workbook [pandas ExcelWriter]

    Return:
        - None
    '''

    # Create a bar chart object
    chart = workbook.add_chart({'type': 'bar'})
    chart.set_style(11)

    # Exclude the row that contains 'Grand Total'
    df_no_total = df[df.iloc[:, 0] != 'Grand Total']

    # Add data series to the chart
    for i in range(1, df_no_total.shape[1]):  
        if df_no_total.columns[i] != 'Grand Total':  # Exclude column with name 'Grand Total'
            chart.add_series({
                'name': [worksheet.name, start[0], start[1] + i],
                'categories': [worksheet.name, start[0] + 1, start[1], start[0] + df_no_total.shape[0], start[1]],  # Include the last row
                'values': [worksheet.name, start[0] + 1, start[1] + i, start[0] + df_no_total.shape[0], start[1] + i],  # Include the last row
            })

    # Set the chart title based on the first column
    title = df_no_total.columns[0]
    chart.set_title({'name': title})

    # Insert the chart into the worksheet
    worksheet.insert_chart(start[0] + df_no_total.shape[0] + 2, start[1] + df_no_total.shape[1] + 2, chart)

def crosstab_reader(workbook:pd.ExcelWriter, df:pd.DataFrame, sheet_name:list[str])->tuple[pd.ExcelWriter, list[pd.ExcelWriter]]:
    '''
    Read multiple crosstab tables in multiple Excel worksheets. 

    Args:
        - workbook: Excel workbook [pandas ExcelWriter]
        - df: Whole dataframe [pandas dataframe]
        - sheet_name: Name of the sheets to read [list]

    Return:
        - workbook: Updated Excel workbook [pandas ExcelWriter]
        - charts: list of Excel charts [pandas ExcelWriter]
    '''

    worksheet = workbook.add_worksheet(sheet_name)

    larr = label(np.array(df.notnull()).astype("int"))
    start_row = 0
    charts = []
    for s in regionprops(larr):
        sub_df = (df.iloc[s.bbox[0]:s.bbox[2], s.bbox[1]:s.bbox[3]].pipe(lambda df_: df_.rename(columns=df_.iloc[0]).drop(df_.index[0])))

        # Bold the column name
        bold = workbook.add_format({'bold': 1})
        # Write the sub_df to the worksheet
        for i, col in enumerate(sub_df.columns):
            worksheet.write(start_row, i, col, bold)
            for j, value in enumerate(sub_df[col]):
                worksheet.write(start_row + j + 1, i, value)

        # Create clustered bar chart for the current table
        generate_bar_chart(sub_df, (start_row, 0), workbook, worksheet)

        # Add some empty rows between tables
        start_row += sub_df.shape[0] + 3
    
    return workbook, charts