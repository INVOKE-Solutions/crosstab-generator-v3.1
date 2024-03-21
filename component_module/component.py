import streamlit as st
from PIL import Image
import pandas as pd
from utils_module.utils import load, demography, col_search, sorter
from component_module.table import write_table


def page_style():
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
    st.title('CrossArt Generator')
    st.image(image)

def page_tabs()->object:
    tab1, tab2 = st.tabs(["Crosstab Generator","Chart Generator"])
    return tab1, tab2

def upload_file()->tuple[pd.DataFrame, object]:
    st.subheader("Upload Survey responses (csv/xlsx)")
    df = st.file_uploader(
        "Please ensure the data are cleaned and weighted (if need to be) prior to uploading."
        )
    if df:
        df_name = df.name
        df = load(df)
        return df, df_name

def weight_selection(df: pd.DataFrame)->str:
    weight = st.selectbox(
        'Select weight column',
        col_search(df, key="weight") + ['Unweighted', '']
        )
    return weight

def demography_selection(df:pd.DataFrame)->list[str]:
    demos = st.multiselect(
        "Choose the demograhic(s) you want to build the crosstabs across",
        list(df.columns) + demography(df),
        demography(df)
        )
    return demos

def demo_sorter(df:pd.DataFrame, demos:list[str])->tuple[int,dict]:
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

def question_selection(df:pd.DataFrame)->tuple[int,int]:
    first = st.selectbox(
        "Select the first question of the survey",
        [''] + list(df.columns)
        )
    if first != '':
        first_idx = list(df.columns).index(first)
        last = st.selectbox(
            "Select the last question of the survey", 
            [''] + list(df.columns)[first_idx + 1:]
            )
        if last != '':
            last_idx = list(df.columns).index(last)
            return first_idx, last_idx
        
def sort_col_by_name(df:pd.DataFrame, first_idx:int, last_idx:int)->list[str]:
    name_sort = st.multiselect(
        "Choose question(s) to sort by name, if any [default: sort by value]", 
        list(df.columns)[first_idx: last_idx + 1], 
        col_search(df[first_idx: last_idx + 1], key="[LIKERT]")
        )
    return name_sort

def num_question(first_idx:int, last_idx:int)->st.subheader:
    st.subheader(
        "Number of questions to build the crosstab on: " + str(
                                last_idx - first_idx + 1
                                ))

def question_list(df:pd.DataFrame, first_idx:int, last_idx:int)->list[str]:
    q_ls = [df.columns[x] for x in range(first_idx, last_idx + 1)]
    return q_ls

def wise_list()->str:
    wise_list = ["% of Column Total","% of Row Total", "Both"]
    wise = st.selectbox(
        "Show values as:", 
        [''] + wise_list
        )
    return wise

def get_multi_answer(df:pd.DataFrame, first_idx:int, last_idx:int)->list[str]:
    multi = st.multiselect(
        "Choose mutiple answers question(s), if any", 
        list(df.columns)[first_idx: last_idx + 1], 
        col_search(df[first_idx: last_idx + 1], key="[MULTI]")
        )
    return multi

def crossgen_tab():
    df, df_name = upload_file()
    if df:
        weight = weight_selection(df)
        if weight != '':
            demos = demography_selection(df)
            if len(demos) > 0:
                score, col_seqs = demo_sorter(df, demos)
                if score == len(demos):
                    first_idx, last_idx = question_selection(df)
                    if last_idx != '':
                        name_sort = sort_col_by_name(
                            df=df,
                            first_idx=first_idx,
                            last_idx=last_idx
                            )
                        num_question(
                            df=df,
                            first_idx=first_idx,
                            last_idx=last_idx
                            )
                        q_ls = question_list(
                            df=df,
                            first_idx=first_idx,
                            last_idx=last_idx
                            )
                        wise = wise_list()
                        if wise != '':
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
                                st.download_button(label='📥 Download', data=df_xlsx, file_name= df_name + '-crosstabs.xlsx')
