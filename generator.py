import streamlit as st
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import xlsxwriter
from chart_module.chart import load_chart, crosstab_reader
from component_module.component import (
    page_style,
    page_tabs,
    crossgen_tab
)

page_style()
tab1, tab2 = page_tabs()

with tab1:
    crossgen_tab()
with tab2:
    st.subheader("Upload Crosstab result in .xlsx format only")
    try:
        st.warning("Please ensure the file contains the **CROSSTAB TABLE**:heavy_exclamation_mark::heavy_exclamation_mark: prior to uploading.", icon="❗")
        df_charts = st.file_uploader("Upload the file here:")

        if df_charts:
            df_chartsname = df_charts.name
            dfs, sheet_names = load_chart(df_charts)
            
            # Create an output Excel workbook
            output = BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})

            # Process each table separately
            for sheet_idx, (sheet_name, df) in enumerate(zip(sheet_names, dfs)):
                workbook, charts = crosstab_reader(workbook, df, sheet_name)
            
            workbook.close()
            df_charts = output.getvalue()
            df_chartsname = df_chartsname[:df_chartsname.find('.')]
            st.balloons()
            st.header('Charts ready for download!')
            st.download_button(label='📥 Download', data=df_charts, file_name= df_chartsname + '-charts.xlsx')

    except:
        st.error('The file should contain the crosstab tables!', icon="🚨")
