# **Cookie Factory - Project Portfolio 3 - Python**

Cookie Factory is a terminal based application tool used for reading instructions, creating new cookie batches and viewing past one. Cookie Factory is used jointly with a google spreadsheet,that contains the data necessary to run the application.

App was deployed in Heroku, please find the link to the project [here.](https://cookie-factory.herokuapp.com/)

If you wish to see the repository and code behind the application you can view it in GitHub [here.](https://github.com/HMuraja/cookie-factory

## User Goals
- Simple tool for simple manufacturing activity/procedure.
- Easy to undertand outputs.
- Minial requirement for user input.
- Possibility to view and review past activities.

## Author Goals
- Demonstrate a tool for manufactruing industry.
- Minimize human error by limiting choices and validating user inputs.
- Reuse of the code and dual functionality.
- Flexible design that could be easily changed as per user needs.

# Features
## Application Design 
I started the project by drafting a a simple flow chart to help me visualize what i wanted to do. The end product doesn't not identcal, but still resembels very much of the original plan. I also wrote the data, meaning instructions and recipes, for the project before even creating a repository for my project. This made it easier to build the code to use that data, and also allowed me to focus more on the code design.

![FlowChart](/assets/readme-media/diagram.jpg)
## Visual Design
As the projects was menat to be made using python, the terminal has been left to minimum. An effort was made to limit the amount of text diplayed on the terminal at once to avoid information overload. All the effects were made by using capital letters, letter spacing, tabs and empty lines. Even though minmal their use was intended to aid the readibility and help in navigation. The emphasis however was kept on the backend side.

## Code Design
-__Input Validation__ I used two functions to validate any input and they are referred throughout the function. One would be validate data and this would validate input that had only few options, like "yes" or "no". The other validatior was used to validate ranged answer options, like number of cookies, when user can choose anything between 10-100. Both of these validators would give an error message DataType and remind what user should enter. I used few other functions to validate the code but they also referred to the two mentioned 

- __Main Menu__ .This the first interface displayed for the user. User is given two options 'View Batches' or 'Bake Cookies'.  After selecting either one of the options user will end up back to the main menu and may select any option they like again. User will choose the option by entering lettering of the options. The input is validated and if anythig lese is entered an Value Error Message is displayed and  correct options displayed. 

- __View Batches__ home menu present user two options to view the past batches: view by month and view last 5 entries. User selects by entering the corresponding letter and if validatuion passes interface changes to either of the follwing.
    - View by Month, displays an input prompt requesting user to  enter year and a month. Inputs are once more validated and date entered formatted and passed to filetrijg function that will print out matchs and inform if there is none. 
    - View last 5 enteris will display five of the most recient entries. No input is required form the user.
    - Returning to Main Menus. After selected data is displayed user can retunr to view batch menu or main menu by selecting corresponding key word. Input is validated.

- __Bake Cookies__ If user chooses to Bake cookies a new interface will display and recipe options are listed. User can once again choose recipe by entering the corresponding letter abreaviation. Input will be validated through one of the two validator functions.
    - Recipes, in total there is three recipes to choose fromk, each represented by abreviation of the recipe name, this abreaviation is required for later point.
    - Employee Input, following the selectuion of the recipe and cookie number, user must enter the intitals of the incolved personnel. Scribe stands for the person reading the instructions and intercating with tha application and operator will the one performing the step action read by the scribe.
    - Cookie Batch Instance is created as soon as all the information preceeding the process have been performed. This instance is needed to run the instruction function. 

-__Run Instructions__ is a function that will coordinate the display of instruction and inputs. This function will run as soon as the CookieBatch Instance has been created.
    - Generate List of Instructions
    - Refer to Recipe
    - If and else for tags
    - Text wrap at 72 characters
    - USer Input
    - Exit Early
    - Save Batch
- __Googl Sheet__
    - recipes
    - batch data
    - instruction steps
    - employees

Cookie Factory was designed to display an exmaple of an batch control for manufacturing, this application could be used in other manufacturing settings that consisst of a procedure with clear steps and some type of ingredient list. Application is easy to understeand and navigate through requireing minmal input from user and providing input validation, limiting any user errors from occurring. Application was designed to be an easy to follow alternative automated replacement for physical batchrecords or instruction manuals. This project and application is may be extended and modified for various uses, depending from the need.

Thsi application has two main actions: bake cookies and view batches. Baking cookies will ultimately lead to creating a new batch that is saved to the batches worksheet. Viewing batches allows users to view previous batches.

# Testing
## Manual
Code was tested throughout the the process to ensure that no errors would occur in the end i did a final testing
## validator Testing
I used [this](https://pep8ci.herokuapp.com/) PEP8 online linter provided by Coding Instritute. Code passed without any issues.

![Pep8 Result](/assets/readme-media/cookie-factory-python-linter.png)

## Bugs
Bugs were fixed in several occasion suring the process. Gitpods error messages and print statements were used as tool to troubleshoot and fix the issues.

# Deployement History

## Gitpod
The project can be deployed in Gitpod.

Following steps were taken to deploy to GitHub page:

 - Find the repository you wish to deploy with Gitpod.
 - Click open the repository and find orange button stating gitpod, clikc on it.
 - A new workspace is uploaded on Gitpod for this project.
 - On the Terminal on Gitpod, type "python3 -m http.server".
 - A pop up request permission to open a port 8000, click open in preview or the browser.

## Github Pages
Live page was deployed in GitHub, as per follows:
 - Find the repository you wish to deploy with Gitpod.
 - Click open the repository and find a "Settings" button on the op ribbon, click on it.
 - Open from the side panel "GitHub Pages" Section.
 - Under "Source", click the "Branch" dropdown and then choose "Master" instead of "None" and press ok.
 - The page will take a while to upload, but once ready a link to the live page will appear on top of the page.

# Credits

## Code
All code has been written by me, unless stated otherwise. If code has been taken elsewhere, it has been clearly stated in this section.

- Code for wrapping long strings of texts into desired lenght was taken from [this](https://stackoverflow.com/questions/32122022/split-a-string-into-pieces-of-max-length-x-split-only-at-spaces) stackoverflow entry.
- In the use of gspread module [this](https://docs.gspread.org/en/latest/user-guide.html#getting-all-values-from-a-row-or-a-column) was referred to often. 

## Resources
Sources for troubleshooting:
 - [W3Schools](https://www.w3schools.com/)
 - [Code Institutes Course Material](https://codeinstitute.net/)

## Content and Media
- Recipes were based on recipe from [sallys baking addiction blog.](https://sallysbakingaddiction.com/chewy-chocolate-chip-cookies/).
- Instruction steps were created by me and inspired by my experience in manufacturing.