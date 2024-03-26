import streamlit as st
from PIL import Image
import pandas as pd
from typing import Any
from utils_module.utils import load, demography, col_search, sorter
from chart_module.chart import load_chart
from component_module.table import write_table
from component_module.viz import draw_chart


def page_style():
    '''
    Streamlit page configuration.

    Args:
        - None

    Return:
        - None
    '''
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
    st.title('CrossArt Generator')
    st.image(image)

def page_tabs()->tuple[Any,Any]:
    '''
    Streamlit tabs configuration on the main page.

    Args:
        - None

    Return:
        - 2 streamlit tabs on the main page.
    '''
    tab1, tab2 = st.tabs(["Crosstab Generator","Chart Generator"])
    return tab1, tab2

def upload_file()->Any:
    '''
    Streamlit component for the user to upload the file.

    Args:
        - None

    Return:
        - df: streamlit dataframe, Uploadedfile sub-class of BytesIO. 
    '''
    st.subheader("Upload Survey responses (csv/xlsx)")
    df = st.file_uploader(
        "Please ensure the data are cleaned and weighted (if need to be) prior to uploading."
        )
    return df
    
def read_file(df:Any)->tuple[pd.DataFrame,str]:
    '''
    Component to read file from streamlit dataframe.

    Args:
        - df: streamlit dataframe, Uploadedfile sub-class of BytesIO. 

    Return:
        - df: pandas dataframe
        - df_name: Name of the uploaded file
    '''
    df_name = df.name
    df = load(df)
    return df, df_name

def weight_selection(df: pd.DataFrame)->str:
    '''
    Component for user to select `weight` column from the dataframe.

    Args:
        - df: pandas dataframe 

    Return:
        - weight: Name of the selected weight column [str]
    '''
    weight = st.selectbox(
        'Select weight column',
        col_search(df, key="weight") + ['Unweighted', '']
        )
    return weight

def demography_selection(df:pd.DataFrame)->list[str]:
    '''
    Component for user to select `demography` column from the dataframe.

    Args:
        - df: pandas dataframe 

    Return:
        - demos: List of name of the selected demography columns.
    '''
    demos = st.multiselect(
        "Choose the demograhic(s) you want to build the crosstabs across",
        list(df.columns) + demography(df),
        demography(df)
        )
    return demos

def demo_sorter(df:pd.DataFrame, demos:list[str])->tuple[int,dict]:
    '''
    Component for user to sort the unique value of `demography` column manually.

    Args:
        - df: pandas dataframe
        - demos: List of name of the selected demography columns.

    Return:
        - score: List of name of the selected demography columns.
        - col_seqs:
            - Key: Demography column
            - Value: Sorted unique value of the key demography column.
    '''
    score = 0
    col_seqs = {}
    for demo in demos:
        st.subheader('Column: ' + demo)
        col_seq = st.multiselect(
            'Please arrange ALL values in order', 
            list(df[demo].unique()), 
            default=sorter(demo, df=df), 
            key = demo
            )
        col_seqs[demo] = col_seq
        if len(col_seq) == df[demo].nunique():
            score += 1
    return score, col_seqs

def q1_selection(df:pd.DataFrame)->str:
    '''
    Component for user to select the column of the first question.

    Args:
        - df: pandas dataframe

    Return:
        - first: Name of the first question column [str]
    '''
    first = st.selectbox(
        "Select the first question of the survey",
        [''] + list(df.columns)
        )
    return first

def qlast_selection(df:pd.DataFrame, first:str)->tuple[int,str]:
    '''
    Component for user to select the column of the last question.

    Args:
        - df: pandas dataframe
        - first: Name of the first question column [str]

    Return:
        - first_idx: Index number of the first question column [int]
        - last: Name of the last question column [str]
    '''
    first_idx = list(df.columns).index(first)
    last = st.selectbox(
            "Select the last question of the survey", 
            [''] + list(df.columns)[first_idx + 1:]
            )
    return first_idx, last

def qlast_index(df:pd.DataFrame, last:str)->int:
    '''
    Get the index of the last question column.

    Args:
        - df: pandas dataframe
        - last: Name of the last question column [str]

    Return:
        - last_idx: Index number of the last question column [int]
    '''
    last_idx = list(df.columns).index(last)
    return last_idx

def sort_col_by_name(df:pd.DataFrame, first_idx:int, last_idx:int)->list[str]:
    '''
    Component for user to select column to sort by the name using keyword `LIKERT`.

    Args:
        - df: pandas dataframe
        - first_idx: Index number of the first question column [int]
        - last_idx: Index number of the last question column [int]

    Return:
        - name_sort: List of column to sort by the name.
    '''
    name_sort = st.multiselect(
        "Choose question(s) to sort by name, if any [default: sort by value]", 
        list(df.columns)[first_idx: last_idx + 1], 
        col_search(df[first_idx: last_idx + 1], key="[LIKERT]")
        )
    return name_sort

def num_question(first_idx:int, last_idx:int)->Any:
    '''
    Component for streamlit to display the number of question column.

    Args:
        - first_idx: Index number of the first question column [int]
        - last_idx: Index number of the last question column [int]

    Return:
        - None.
    '''
    st.subheader(
        "Number of questions to build the crosstab on: " + str(
                                last_idx - first_idx + 1
                                ))

def question_list(df:pd.DataFrame, first_idx:int, last_idx:int)->list[str]:
    '''
    Get the list of question.

    Args:
        - df: pandas dataframe
        - first_idx: Index number of the first question column [int]
        - last_idx: Index number of the last question column [int]

    Return:
        - q_ls: List of question column.
    '''
    q_ls = [df.columns[x] for x in range(first_idx, last_idx + 1)]
    return q_ls

def wise_list()->str:
    '''
    Component for user to choose the value options for the crosstabs.

    Args:
        - None.

    Return:
        - wise: User selection of the value options.
    '''
    wise_list = ["% of Column Total","% of Row Total", "Both"]
    wise = st.selectbox(
        "Show values as:", 
        [''] + wise_list
        )
    return wise

def get_multi_answer(df:pd.DataFrame, first_idx:int, last_idx:int)->list[str]:
    '''
    Component for user to select column that contains multiple answer option using keyword `MULTI`.

    Args:
        - df: pandas dataframe
        - first_idx: Index number of the first question column [int]
        - last_idx: Index number of the last question column [int]

    Return:
        - multi: List of column that contains multiple answer option.
    '''
    multi = st.multiselect(
        "Choose mutiple answers question(s), if any", 
        list(df.columns)[first_idx: last_idx + 1], 
        col_search(df[first_idx: last_idx + 1], key="[MULTI]")
        )
    return multi

def init_crossgen_tab():
    '''
    Composite function to run the front-end of the crosstabs streamlit based on logic. 

    Args:
        - None

    Return:
        - None
    '''
    df = upload_file()
    if df:
        df, df_name = read_file(df=df)
        weight = weight_selection(df=df)
        if weight:
            demos = demography_selection(df=df)
            if len(demos) > 0:
                score, col_seqs = demo_sorter(df=df, demos=demos)
                if score == len(demos):
                    first = q1_selection(df=df)
                    if first:
                        first_idx, last = qlast_selection(df=df, first=first)
                        if last:
                            last_idx = qlast_index(df=df, last=last)
                            if last_idx:
                                name_sort = sort_col_by_name(
                                    df=df,
                                    first_idx=first_idx,
                                    last_idx=last_idx
                                    )
                                num_question(
                                    first_idx=first_idx,
                                    last_idx=last_idx
                                    )
                                q_ls = question_list(
                                    df=df,
                                    first_idx=first_idx,
                                    last_idx=last_idx
                                    )
                                wise = wise_list()
                                if wise:
                                    multi = get_multi_answer(
                                        df=df,
                                        first_idx=first_idx,
                                        last_idx=last_idx
                                        )
                                    button = st.button('Generate Crosstabs')
                                    if button:
                                        df_xlsx = write_table(
                                            df=df,
                                            demos=demos,
                                            wise=wise,
                                            q_ls=q_ls,
                                            multi=multi,
                                            name_sort=name_sort,
                                            weight=weight,
                                            col_seqs=col_seqs
                                            )
                                        df_name = df_name[:df_name.find('.')]
                                        st.balloons()
                                        st.header('Crosstabs ready for download!')
                                        st.download_button(
                                            label='📥 Download', 
                                            data=df_xlsx, 
                                            file_name= df_name + '-crosstabs.xlsx'
                                            )
                                        
#--------------------Component for Chart Generator-------------------
def issue_warning()->Any:
    '''
    Streamlit component to warn user regarding the type of uploaded file. 

    Args:
        - None

    Return:
        - streamlit subheader display.
    '''
    st.subheader(
        "Upload Crosstab result in .xlsx format only"
    )

def upload_crosstabs()->pd.DataFrame:
    '''
    Streamlit component for the user to upload file that contains crosstabs table.

    Args:
        - None

    Return:
        - df_charts: streamlit dataframe, Uploadedfile sub-class of BytesIO. 
    '''
    st.warning(
        "Please ensure the file contains the **CROSSTAB TABLE**:heavy_exclamation_mark::heavy_exclamation_mark: prior to uploading.", 
        icon="❗"
        )
    df_charts = st.file_uploader("Upload the file here:")
    return df_charts

def error_warning()->st.error:
    '''
    Streamlit component to display error to user when the uploaded file did not contain crosstabs table. 

    Args:
        - None

    Return:
        - streamlit error display.
    '''
    st.error(
        "The file should contain the crosstab tables!", 
        icon="🚨"
        )

def init_chart_gen():
    '''
    Composite function to run the front-end of the chart generator streamlit based on logic. 

    Args:
        - None

    Return:
        - None
    '''
    issue_warning()
    try:
        df_charts = upload_crosstabs()
        if df_charts:
            dfs, sheet_names, df_chartsname = load_chart(df_charts=df_charts)
            df_charts = draw_chart(dfs=dfs, sheet_names=sheet_names)
            df_chartsname = df_chartsname[:df_chartsname.find('.')]
            st.balloons()
            st.header("Charts ready for download!")
            st.download_button(
                label='📥 Download', 
                data=df_charts, 
                file_name= df_chartsname + '-charts.xlsx'
                )
    except:
        error_warning()
