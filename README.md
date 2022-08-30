# Crosstab Generator Version 2

An upgraded version of the previous crosstab generator 

You can access the crosstab generator through the link below <br />
🠊 https://invoke-analytics-crosstabs-prod-generator-cs1fpd.streamlitapp.com/

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
4. **invoke_logo.jpg** <br />
   Invoke logo to be imported into generator.py
5. **requirements.txt** <br />
   List of the libraries and their respected versions required for the project

### Progress

**Some features that are available in the version 2 of crosstab generator:**

1. User can select the values to be shown in either % of total column, % of total row or both
2. The crosstable automatically removes blank cells in filtered question, so they are not included in the calculations

**Feedbacks for future development ideas:**

**1. Pre-selection on:**
   * Weight column. Automatically select the weight column if detected
   * 3 basic demographic columns. Automatically select gender, agegroup and ethgroup
     columns if detected
   * Multiple answer questions. Automatically detect [MULTI]
   
**2. Automatic Column Sequence:**
   * gender - sort from Z-A (Male, Female)
   * agegroup - sort from A-Z (ascending order)
   * ethgroup - sort in the following sequence (Malay, Chinese, Indian, Bumiputera or Others)
   
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

1. Firstly, fork this repository. Make sure the owner of the repository is INVOKE-Analytics.

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
