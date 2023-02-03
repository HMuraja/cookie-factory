# 79 79 79 79 79 79 79 -- MAX width of your terminal-- 79 79 79 79 79 79 79 79
# External libraries to access google sheets
import gspread
from google.oauth2.service_account import Credentials

# Contstant variables for credentials and APIs
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('cookie_batches')

# The three available recipes are listed below as constant variables
COOKIE_PROTOCOL = {
    "Classic Cookies": {
        "wet ingredients": {
            "Butter": 0.16,
            "Vanilla Extract": 0.005,
            "Egg Mix": 0.10,
            "Light Brown Sugar": 0.16},
        "dry ingredients": {
            "Flour": 0.38,
            "Baking Powder": 0.003,
            "Baking Soda": 0.002,
            "White Chocolate": 0.19}},
    "Raspberry and White Chocolate Cookies": {
        "wet ingredients": {
            "Butter": 0.16,
            "Vanilla Extract": 0.005,
            "Raspberries": 0.10, 
            "White Sugar": 0.16}, 
        "dry ingredients": {
            "Flour": 0.38,
            "Baking Powder": 0.003,
            "Baking Soda": 0.002,
            "White Chocolate": 0.19}},
    "Peanut Butter Cookies": {
        "wet ingredients": {
            "Butter": 0.18,
            "Vanilla Extract": 0.005,
            "Egg Mix": 0.11,
            "Light Brown Sugar": 0.16},
        "dry ingredients": {
            "Flour": 0.30,
            "Cacao Powder": 0.05,
            "Baking Powder": 0.003,
            "Baking Soda": 0.002,
            "Reesee’s Chips": 0.19}}}

# Set up APIs
batches = SHEET.worksheet('batches')
batch_data = batches.get_all_values()

# Script for the Cookie Factory Terminal starts from here


def start_menu():
    """
    Function prints out the main menu presenting the user the
    available activities
    """
    print("---------COOKIE FACTORY TERMINAL---------")
    print("Welcome to the Cookie Factory’s procedure terminal!")
    print("Available actions:")
    print("\t a.	Bake Cookies")
    print("\t b.	View Batches")

    while True:
        choice = input("\nSelect an action by entering a or b:\n")
        if validate_data(choice, "a or b", "a", "b"):
            if choice == "a":
                print("\nUploading available Recipes...\n")
            else:
                print("\nUploading batch data...(Batches Code not buld yet)\n")
            break
    return choice


def validate_data(data, answer_string, *expected_input):
    """
    Checks if the data entered is a or b, the only data
    accepted.
    """
    try:
        for expectation in expected_input:
            if data == expectation:
                return True
        raise ValueError(
            f"Please enter {answer_string}"
            )
    except ValueError as e:
        print(f"\nInvalid data! {e}, please try again.")
        return False  


def validate_cookie_range(data, answer_string):
    """
    Checks if the data entered is a value 10-100
    """
    try:
        if data >= 10 and data <=100:
            return True
        raise ValueError(
            f"Please enter {answer_string}"
            )
    except ValueError as e:
        print(f"\nInvalid data! {e}, please try again.")
        return False


def select_recipe():
    """
    Displays all available recipes and expect user input.
    User input is validated by running user input trhough validate_data 
    function.
    """
    print("---------Choose a Protocol---------")
    print("\nAvailable recipes:")
    print("\t1.	Classic Cookies")
    print("\t2.	Raspberry and White Chocolate Cookies")
    print("\t3.	Peanut Butter Cookies")
    while True:
        choice = int(input(
            "\nPlease select a recipe by entering the corresponding number: "))
        if validate_data(choice, "1, 2 or 3", 1, 2, 3):
            recipe_name = list(COOKIE_PROTOCOL.keys())[choice-1]
            break
    while True:
        amount = int(input(
            "\nHow many cookies you plan to prepare min 10 max 100): "))
        if validate_cookie_range(amount, "number from 10-100"):
            print(f"\nUploading procedure for {amount} {recipe_name}...\n")
            return (amount, recipe_name)       


def manufacture_cookies(cookie_protocol):
    """Step instructions to manufacture cookies"""
    #The recipe selected
    recipe = COOKIE_PROTOCOL[cookie_protocol[1]]
    #Total wight of the dough when one cookie is 90g
    weight = cookie_protocol[0] * 90 
    next_line = "\n\tPress enter to move onto next step"
    wet_ingredients = recipe["wet ingredients"]
    dry_ingredients = recipe["dry ingredients"]

    #Instructions start from here
    print(f"---------Running {cookie_protocol[1]} Protocol---------")
    input("Press enter once ready to start")
    print("\n(Step 1) Gather the following Ingredients:")
    for ingredient in wet_ingredients.keys():
        print(f"\n\t {ingredient}")
    for ingredient in dry_ingredients.keys():
        print(f"\n\t {ingredient}")
    input(next_line)

    print("\n(Step 2) Check that mixer and the work station is")
    print("\tclean & free of particles.")
    input(next_line)

    print("\n(Step 3) Measure and place the following ingredients into the mixer:")
    for ingredient, amount in recipe["wet ingredients"].items():
        print(f"\n\t{ingredient} \t{amount * weight}g")
    input(next_line)

    mixing_step(5, 4)

    print("\n(Step 7) While the mixer is running")
    print("\tmeasure and place following ingredients to the measuring bowl:")
    for ingredient, amount in recipe["dry ingredients"].items():
        print(f"\n\t{ingredient}\t\t{amount * weight}g")

    print("\n(Step 8)Mix the dry ingredients using a whisker.")
    input(next_line) 

    print("\n(Step 9)Once mixer timer has finished, open the")
    print("\tguard and place the dry ingredients on top of the wet ingredients.")
    input(next_line) 

    mixing_step(2, 10)

    


def mixing_step(time, first_step_no):
    """Function for printing the  mixing steps"""
    print(f"\n(Step{first_step_no}) Set the mixer speed to number two")
    print(f"\tclose the guard and set the timer for {time} minutes.")
    print("\tPress start.")
    input("\n\tPress enter to move onto next step")

    print(f"\n(Step{first_step_no + 1}) Once timer has finished and mixer")
    print("\thas stopped. Open the guard and use a spatula")
    print("\tto scrape any dough on the sides down into bottom")
    input("\n\tPress enter to move onto next step")

    print(f"\n(Step{first_step_no + 2}) Close the guard,")
    print("\tconfirm speed is 2 and set the timer for 5 minutes.")
    print("\tPress start.")
    input("\n\tPress enter to move onto next step")


def main():
    """
    Runs the terminal functions
    """
    #terminal_action = start_menu()
    #if terminal_action == "a":
        #protocol_info = select_recipe()
    protocol_info = (11, "Raspberry and White Chocolate Cookies")
    manufacture_cookies(protocol_info)


main()
