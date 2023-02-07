# 79 79 79 79 79 79 79 -- MAX width of your terminal-- 79 79 79 79 79 79 79 79
# External libraries to access google sheets
import math
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
    except ValueError as error:
        print(f"\nInvalid data! {error}, please try again.")
        return False  


def validate_range(data, min_range, max_range):
    """Validates a data that should be within certain range"""
    try:
        if (int(data) or data == "0") and int(data) in range(min_range, (max_range+1)):
            return True
        raise ValueError(f"Please enter {min_range}-{max_range}")
    except ValueError as error:
        print(f"\nInvalid data! {error}, please try again.")
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
        if validate_range(amount, 10, 100):
            print(f"\nUploading procedure for {amount} {recipe_name}...\n")
            return (amount, recipe_name)       


def start_manufacturing(cookie_protocol):
    """Step instructions to manufacture cookies"""
    recipe = COOKIE_PROTOCOL[cookie_protocol[1]]
    next_line = "\n\tPress enter to move onto next step "

    print("R U N N I N G   P R O T O C O L:")
    print(f"\t{cookie_protocol[1]}")
    input("\n\tPress enter once ready to start.\n\n")
    
    print("\t\n(Step 1)\n\tGather the following Ingredients:")
    for ingredient in recipe["wet ingredients"].keys():
        print(f"\n\t {ingredient}")
    for ingredient in recipe["wet ingredients"].keys():
        print(f"\n\t {ingredient}")
    input(next_line)

    print("\t\n(Step 2)\n\tCheck that mixer and the work station is clean &")
    print("\tfree of particles.")
    input(next_line)


def mix_ingredients(cookie_protocol):
    """Instructions for handing the dry ingredients"""
    recipe = COOKIE_PROTOCOL[cookie_protocol[1]]
    weight = cookie_protocol[0] * 90
    next_line = "\n\n\tPress enter to move onto next step "
    
    print("\t\n(Step 3)\n\tMeasure & place the following into the mixer:")
    for ingredient, amount in recipe["wet ingredients"].items():
        print(f"\n\t{ingredient} - {amount * weight}g")
    input(next_line)

    mixing_step(5, 4)

    print("\t\n(Step 7)\n\tWhile the mixer is running measure and place")
    print("\tfollowing ingredients to the measuring bowl:")
    for ingredient, amount in recipe["dry ingredients"].items():
        print(f"\n\t{ingredient}\t\t{amount * weight}g")

    print("\t\n(Step 8)\n\tMix the dry ingredients using a whisker.")
    input(next_line)

    print("\n\t\n(Step 9)\n\tOnce mixer timer has finished, open the guard")
    print("\tand pour the dry ingredients on top of the wet ingredients.")
    input(next_line)

    mixing_step(2, 10)

    print("\t\n(Step 13)\n\tOpen the guard and remove the mixing bowl")
    print("\tremove from the machine onto a trolley.")
    input(next_line)


def bake_and_store(cookie_protocol):
    """Instructions to bake, store and label the cookies"""
    weight = cookie_protocol[0] * 90
    next_line = "\n\tPress enter to move onto next step "

    #Count how many pans do you need, when each pan can take 10 cookies
    print(f"\t\n(Steps 14)\n\tPlace {math.ceil(weight/90/10)} tray on the work")

    print("\tsurface and place a baking sheet on top of each one.")
    input(next_line)
    
    print("\t\n(Step 15)\n\tPlace one scoop of cookie dough on the scale.")
    print("\tAdd or remove dough until it weights around 85-95g.")
    print("\tPlace the measured dough on the baking sheet.")
    print("\tRepeat the process until dough is finished.")
    print("\tIF the last cookie is less than 85 g, discard this dough.")
    input(next_line)

    while True:
        cookies_made = input("\n\tEnter the amount of cookies prepared:\t")
        if validate_range(cookies_made, 0, cookie_protocol[0]):
            print("\tData valid!Please proceed!")
            break
    print("\t\n(Step 16)\n\tPlace the tray in a trolley and transport them")
    print("\tnext to the ovens.")
    print("\tOne by one place the pans in the oven.")
    print("\tSet the timer for 12 minutes.")
    input(next_line)

    print("\t\n(Step17)\n\tUsing oven-mittens remove the pans from the oven ")
    print("\tand place them in the trolley.")
    print("\tInspect the cookies and discard any burnt or disfigured ones.")
    while True:
        cookies_discarded = input("\tEnter the amount of cookies discarded:\t")
        print(cookies_discarded)
        print(cookies_made)
        if validate_range(cookies_discarded, 0, int(cookies_made)):
            print("\tEntered data valid!Please proceed!")
            if cookies_discarded == cookies_made:
                choice = input("All cookies dicarded? Type yes or no:")
                if validate_data(choice, "yes or no"):
                    if choice == "yes":
                        print("Process finished!")
                        main()
                    else:
                        continue
            break
    input(next_line)

    print("\t\n(Step19)\n\tTransport the trolley in the storage area")
    print("\tlabel the trolley with batch number{batch_no}.")
    print("\tSet the timer for 1 hour.")
    input(next_line)

    print("\t\n(Step 20)\n\tOnce time is up, place cookies in storage boxes")
    print("\tand label each one with the following information:")
    print("\tBatch Number:")
    print(f"\tType: \t{cookie_protocol[1]}")
    print("\tManufacturing date:")
    input(next_line)

    print("\n\tProcess finished!")
    return [cookies_made, cookies_discarded]


def save_batch_data(batch_no):
    while True:
        entry = input(
            "\t Type yes/no if you wish to save the batch information: ")
        if validate_data(entry, "yes or no", "yes", "no"):
            print(f"Save here the batch data{batch_no}")
            break


def mixing_step(time, first_step_no):
    """Function for printing the  mixing steps"""
    print(f"\t\n(Step {first_step_no})\n\tSet the mixer speed to number two and")
    print(f"\tclose the guard and set the timer for {time} minutes.")
    print("\tPress start.")
    input("\n\tPress enter to move onto next step ")

    print(f"\t\n(Step {first_step_no + 1})\n\tOnce timer has finished and mixer")
    print("\thas stopped. Open the guard and use the spatula")
    print("\tto scrape the mixture on the sides down into the bottom.")
    input("\n\tPress enter to move onto next step ")

    print(f"\t\n(Step {first_step_no + 2})\n\tClose the guard, confirm speed")
    print(f"\tis fixed to 2 and set the timer for {time} minutes.")
    print("\tPress start.")
    input("\n\tPress enter to move onto next step ")


def main():
    """
    Runs the terminal functions
    """
    #terminal_action = start_menu()
    #if terminal_action == "a":
        #protocol_info = select_recipe()
    protocol_info = (11, "Raspberry and White Chocolate Cookies")
   #start_manufacturing(protocol_info)
    #mix_ingredients(protocol_info)
    bake_and_store(protocol_info)
    #save_batch_data(batch_no):


main()
