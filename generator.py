import streamlit as st
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
from PIL import Image
import xlsxwriter
from utils_module.utils import load, demography, col_search, sorter, get_row, get_column
from chart_module.chart import load_chart, crosstab_reader

# Hide streamlit header and footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

# configure the default settings of the page.
icon = Image.open('photos/invoke_icon.jpg')
st.set_page_config(page_icon=icon)

st.markdown(hide_st_style, unsafe_allow_html=True)

image = Image.open('photos/invoke_logo.png')
st.title('Crosstabs Generator')
st.image(image)
tab1, tab2 = st.tabs(["Crosstab Generator","Chart Generator"])

with tab1:
    st.subheader("Upload Survey responses (csv/xlsx)")
    df = st.file_uploader("Please ensure the data are cleaned and weighted (if need to be) prior to uploading.")
    if df:
        df_name = df.name
        df = load(df)
        weight = st.selectbox('Select weight column', col_search(df, key="weight") + ['Unweighted', ''])
        if weight != '':
            demos = st.multiselect('Choose the demograhic(s) you want to build the crosstabs across', list(df.columns) + demography(df), demography(df))
            
            if len(demos) > 0:
                # Ensure that all the demographic values have been selected before proceeding
                score = 0
                col_seqs = {}
                for demo in demos:
                    st.subheader('Column: ' + demo)
                    col_seq = st.multiselect('Please arrange ALL values in order', list(df[demo].unique()), default=sorter(demo, df=df), key = demo)
                    col_seqs[demo] = col_seq
                    if len(col_seq) == df[demo].nunique():
                        score += 1

                if score == len(demos):
                    first = st.selectbox('Select the first question of the survey',[''] + list(df.columns))
                    if first != '':
                        first_idx = list(df.columns).index(first)
                        last = st.selectbox('Select the last question of the survey', [''] + list(df.columns)[first_idx + 1:])
                        if last != '':
                            last_idx = list(df.columns).index(last)
                            st.subheader('Number of questions to build the crosstab on: ' + str(last_idx - first_idx + 1))
                            q_ls = [df.columns[x] for x in range(first_idx, last_idx + 1)]
                            wise_list = ['% of Column Total','% of Row Total', 'Both']
                            wise = st.selectbox('Show values as:', [''] + wise_list)
                            if wise != '':
                                multi = st.multiselect('Choose mutiple answers question(s), if any', list(df.columns)[first_idx: last_idx + 1], col_search(df[first_idx: last_idx + 1], key="[MULTI]"))
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
                                                    start, workbook, worksheet = get_column(df, q, multi, demo, weight, col_seqs, writer, start)

                                                start_2 = 1
                                                for q in q_ls:
                                                    start_2, workbook, worksheet = get_row(df, q, multi, demo, weight, col_seqs, writer, start_2)
                                            
                                            elif wise == '% of Column Total':
                                                start = 1
                                                for q in q_ls:
                                                    start, workbook, worksheet = get_column(df, q, multi, demo, weight, col_seqs, writer, start)

                                            else:
                                                start_2 = 1
                                                for q in q_ls:
                                                    start_2, workbook, worksheet = get_row(df, q, multi, demo, weight, col_seqs, writer, start_2)
                                    
                                    writer.save()
                                    df_xlsx = output.getvalue()
                                    df_name = df_name[:df_name.find('.')]
                                    st.balloons()
                                    st.header('Crosstabs ready for download!')
                                    st.download_button(label='📥 Download', data=df_xlsx, file_name= df_name + '-crosstabs.xlsx')

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



