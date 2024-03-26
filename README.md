# Crosstab Generator Version 3

An upgraded version of the previous crosstab generator 

You can access the crosstab generator through the link below <br />
🠊 https://invoke-analytics-crosstab-generator-v3-generator-6pyb9x.streamlit.app/

## What is Crosstab?

Crosstab is a two- (or more) dimensional table that is usually used in data analysis to uncover more granular insights from the data we gathered from the survey. It makes use of a statistical analysis known as Cross Tabulation analysis (or also known as Contingency Table analysis) to quantitatively evaluate the correlation between multiple variables. A typical cross-tabulation table compares two hypothetical variables, which are usually the survey question and the respondents' demographic (it can be either ethnicity, age group, gender, etc). 

## About the Project

This project aims to expedite our crosstab generation process from long minutes of manual labour work using Excel pivot table to just a mere couple of seconds. With this crosstab generator, one just need to upload the weighted data file, wait for a couple of seconds and boom - the crosstab is set for you! By automating the crosstab generation process, we hope to divert the time and energy that are previously used for crosstab to other purposes, so that we can improve our overall survey work.

### File Descriptions

1. **.streamlit** <br />
   Set the default theme to dark
2. **README.md** <br />
   Project documentation
3. **generator.py** <br />
   Project code
4. **photos** <br />
   Contains INVOKE Analytics logo and INVOKE logo to be imported into generator.py
5. **requirements.txt** <br />
   List of the libraries and their respective versions required for the project
6. **crosstab_module** <br />
Contains all of the main functions to create the crosstabs.
7. **utils_module** <br />
Contains all of the helper functions for the crosstabs generator. Also, contains the processor functions that call functions from crosstab.py and utils.py
8. **chart_module** <br />
Contains all of the functions to create the clustered bar charts. 
9. **component_module** <br />
Contains all of the components; front-end component for streamlit and back-end component for crosstabs and charts. 

### Folder Structure

```
.
├── README.md
├── .streamlit/
│   └── config.toml
├── .github/
│   └── dependabot.yml
├── chart_module/
│   └── chart.py
├── crosstab_module/
│   └── crosstab.py
├── component_module/
│   └── component.py
│   └── table.py
│   └── viz.py
├── photos/
│   ├── invoke_icon.jpg
│   └── invoke_logo.png
├── utils_module/
│   ├── processor.py
│   └── utils.py
├── generator.py
└── requirements.txt
```

### Progress

**Some features that are available in the version 3 of crosstab generator:**

**1. Pre-selection on:**
   * Weight column. Automatically select the weight column if detected
   * 5 basic demographic columns. Automatically select age group, gender, ethnicity group, income group and urbanity
     columns if detected
   * Multiple answer questions. Automatically detect columns with keyword=[MULTI]
   * Column to sort by name. Automatically detect columns with keyword=[LIKERT]
     
**2. Automatic Column Sequence in Malay and English:**
   * Gender - sort from Male to Female/M to F/Lelaki to Perempuan/L to P
   * Age group - sort from A-Z (ascending order)
   * Ethnicity group - sort in the following sequence (Malay, Chinese, Indian, Bumiputera or Others) or (Melayu, Cina, India, Bumiputera or Lain-Lain)

**3. Automatic Generate Clustered Bar Chart based on the Crosstab Tables:**
   * Automation of the clustered bar chart creation in reference to the generated crosstab table. 

**4. Modularize the function:**
   * Tidy up the functions for the crosstab and chart generator by putting in different modules.

**5. Sort the order of crosstabs table:**
   * User can choose which column to sort by name [default sorting option is sorting by value].


### ⚠ Attention

1. Before uploading your Excel file, make sure that the demographic column name characters is less than 10 chars. Exceeding chars will lead to error due to Excel formatting. 
2. On _Select column weight_ section choice, `Unweighted` choice has some unsettled bugs. Hence, if your dataset is _Unweighted_, create one extra column name *weight* with all value 1. Then choose this column name for this part.

**Feedbacks for future development ideas:**

**1. Add chart options for user to choose:**
* [ ]  Add new charts features such as pie chart. 

**2. Add new demography in the demography sorter function for automation:**
* [ ]  State demography.
 
**3. Combine of survey weighting platform and crosstabs generator:**
* [ ]  Create APIs for crosstabs geerator and survey weighting platform.

### Built With

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://invoke-analytics-crosstabs-prod-generator-cs1fpd.streamlitapp.com/)

## Getting Started

If you are working on this project, simply follow the guide below.

### Prerequisites

1. Github Account
2. Git Bash
3. Visual Studio Code
4. Streamlit Cloud (Only for deployment stage)

### Installations

1. **Github Account** <br />
   If you are reading this document, that means you already have a Github account. Congratss!! :partying_face::tada: But if you simple want to create a new account,      click [here](https://docs.github.com/en/get-started/onboarding/getting-started-with-your-github-account) for more information about it.
   
2. **Git Bash** <br />
   If you have never heard of it before, Git Bash is a source control management system for Windows that allows users to type Git commands (such as git clone and git      commit) which we will use a lot in this project. To install it, download the Git Bash setup from the official website: https://git-scm.com/

3. **Visual Studio Code** <br />
   This is the suggested IDE for this project. The reason for this is because Visual Studio Code works seamlessly with Git since there is a Git Bash extension that you    can easily install in it. You can go to this [page](https://code.visualstudio.com/download) to download Visual Studio Code that matches your operating system. 
   
4. **Streamlit Cloud** (Only for deployment stage) <br />
   There are a lot of public cloud platforms out there that you can use to deploy your Streamlit app. However, in this project, we use Streamlit Cloud since it is free 
   and easy to manage. You need to create a Streamlit Cloud account in order to deploy a new Streamlit app as well as to monitor other Streamlit apps in our existing 
   Invoke Analytics repositories. To create an account, simply sign up once you click this [link](https://code.visualstudio.com/download).
   
### Contributions

Once you have met all of the prerequisites and completed the installations, you can now start working on the project. 

1. Firstly, fork this repository. Make sure the owner of the repository is INVOKE-Solutions.

2. Create a new folder on your local computer.

3. Open Visual Studio Code, click Open Folder and choose the folder that you just created.

4. Open Git Bash terminal.

5. Clone your forked repository into the folder by applying the git command below.

   ```
   git clone your-forked-repo-url
   ```
   
6. Now, a copy of all the files should appear on your folder. The next step is to create a separate version of the repository that is usually called branch. This will 
   be the place where you will be working on your code. To do this, go to the python file (generator.py) by using 
   ```
   cd generator.py
   ```
   
7. To create a new branch, simply type
   ```
   git checkout -b branch-name
   ```

8. Congrats!! Now you are in your newly isolated branch. You can freely edit your code over here.

9. After you have finished editing the code, it is now time to push it into your forked repository. You can do that firstly by performing the two lines below
   ```
   git add generator.py
   git commit -m 'your-message'
   ```
 
10. The next step would be to update your code in the local main. You can go to your local main by using
    ```
    git checkout main
    ```
   
11. After that, you can update the local main by merging the main with the branch. You can use the code below.
    ```
    git merge branch-name
    ```

12. Boom!! :confetti_ball: Now, your code has been updated into the local main. You just have one step left in your bucket. To finish off, you need to push the 
    code from your local computer to your forked Github repository (remote). Just write
    ```
    git push
    ```

### Acknowledgement
* [Amer Wafiy - Original Author](https://github.com/amerwafiy)
* [Zabir Azreen - Crosstabs V2](https://github.com/zabirazreen/crosstabs)
* [Sim Lin Zheng - Tablo](https://github.com/linzheng1009/Tablo)
* [Safwan Shamsir - Crosstab V3](https://github.com/safwanshamsir99)

