# 79 79 79 79 79 79 79 -- MAX width of your terminal-- 79 79 79 79 79 79 79 79
# External libraries to access google sheets
import math
from datetime import date
import os
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
    "1": {
        "abbreviation": "cl",
        "name": "Classic Cookies",
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
    "2": {
        "abbreviation": "rw",
        "name": "Raspberry and White Chocolate Cookies",
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
    "3": {
        "abbreviation": "rw",
        "name": "Peanut Butter Cookies",
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
    print("---------C O O K I E   F A C T O R Y   T E R M I N A L---------")
    print("\nWelcome to the Cookie Factory’s procedure terminal!")
    print("Available actions:")
    print("\t a.	Bake Cookies")
    print("\t b.	View Batches")

    while True:
        choice = input("\nSelect an action by entering a or b:\n")
        if validate_data(choice, "a or b", ["a", "b"]):
            if choice == "a":
                print("\nUploading available Recipes...\n")
            else:
                print("\nUploading batch data...(Batches Code not buld yet)\n")
            break
    
    os.system('cls')
    return choice


def validate_data(data, answer_string, *expected_input):
    """
    Expected_input tuple is unloaded into expected list.
    Checks if the data entered is in the expected list.
    Returns error if data can't be found. 
    """
    expected_list = expected_input[0]
    try:
        for expectation in expected_list:
            if data == expectation:
                return True
        raise ValueError(
            f"\n\tPlease enter {answer_string}"
            )
    except ValueError as error:
        print(f"\n\tInvalid data! {error}, please try again.\n")
        return False  


def validate_range(data, min_no, max_no):
    """Validates a data that should be within certain range"""
    try:
        if (int(data) or data == "0") and int(data) in range(min_no, max_no + 1):
            return True
        raise ValueError(f"Please enter {min_no}-{max_no}")
    except ValueError as error:
        print(f"\nInvalid data! {error}, please try again.")
        return False


def select_recipe():
    """
    Displays all available recipes and expect user input.
    User input is validated by running user input trhough validate_data 
    function.
    """
    print("---------P R O T O C O L S   A V A I L A B L E---------")
    print("\nAvailable recipes:")
    print("\t1.	Classic Cookies")
    print("\t2.	Raspberry and White Chocolate Cookies")
    print("\t3.	Peanut Butter Cookies")
    while True:
        choice = input(
            "\nPlease select a recipe by entering the corresponding number: \n")
        if validate_data(choice, "1, 2 or 3", ['1', '2', '3']):
            cookies_dict = COOKIE_PROTOCOL[str(choice)]
            recipe_name = cookies_dict["name"]
            break
    while True:
        amount = input(
            "\nHow many cookies you plan to prepare min 10 max 100): \n")
        if validate_range(amount, 10, 100):
            print(f"\nUploading procedure for {amount} {recipe_name}...\n")
            return (amount, str(choice))       


def start_manufacturing(cookie_protocol):
    """Step instructions to manufacture cookies"""
    recipe = COOKIE_PROTOCOL[cookie_protocol[1]]
    next_line = "\n\tPress enter to move onto next step \n"

    input("\n\tPress enter once ready to start.\n")
    print("\n\tS T A R T I N G   P R O T O C O L:")
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
    weight = int(cookie_protocol[0]) * 90

    next_line = "\n\n\tPress enter to move onto next step " 
    print("\t\n(Step 3)\n\tMeasure & place the following into the mixer:")
    for ingredient, amount in recipe["wet ingredients"].items():
        print(f"\n\t{ingredient} - {amount * weight}g")
    input(next_line)

    mixing_step(5, 4)

    print("\t\n(Step 7)\n\tWhile the mixer is running measure and place")
    print("\tfollowing ingredients to the measuring bowl:")
    for ingredient, amount in recipe["dry ingredients"].items():
        ingredient_weight = round((amount * weight), 2)
        print(f"\n\t{ingredient}\t\t{ingredient_weight}g")

    print("\t\n(Step 8)\n\tMix the dry ingredients using a whisker.")
    input(next_line)

    print("\n\t\n(Step 9)\n\tOnce mixer timer has finished, open the guard")
    print("\tand pour the dry ingredients on top of the wet ingredients.")
    input(next_line)

    mixing_step(2, 10)

    print("\t\n(Step 13)\n\tOpen the guard and remove the mixing bowl")
    print("\tremove from the machine onto a trolley.")
    input(next_line)


def bake_and_store(cookie_protocol, batch_data):
    """Instructions to bake, store and label the cookies"""
    weight = int(cookie_protocol[0]) * 90
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
        cookies_made = input("\n\tEnter the amount of cookies prepared:\n")
        if validate_range(cookies_made, 0, int(cookie_protocol[0])):
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
        cookies_discarded = input("\n\tEnter the amount of cookies discarded:\n")
        if validate_range(cookies_discarded, 0, int(cookies_made)):
            print("\n\tEntered data valid!Please proceed!")
            if cookies_discarded == cookies_made:
                while True:
                    choice = input("\n\tAll cookies dicarded? Type yes or no: \n")
                    if validate_data(choice, "yes or no", ["yes", "no"]):
                        if choice == "yes":
                            batch_data.extend([cookies_made, cookies_discarded, "no"])
                            print("\n\tProcess finished!")
                            return batch_data
                    break
            else: 
                break
    input(next_line)

    print("\t\n(Step19)\n\tTransport the trolley in the storage area")
    print("\tlabel the trolley with batch number{batch_no}.")
    print("\tSet the timer for 1 hour.")
    input(next_line)

    print("\t\n(Step 20)\n\tOnce time is up, place cookies in storage boxes")
    print("\tand label each one with the following information:")
    print(f"\tBatch Number:\t\t{batch_data[2]}")
    print(f"\tType: \t\t\t{batch_data[1]}")
    print(f"\tManufacturing date: \t{batch_data[0]}")
    input(next_line)
    
    batch_data.extend([cookies_made, cookies_discarded, "yes"])
    return batch_data


def mixing_step(time, first_step_no):
    """Function for printing the  mixing steps"""
    print(f"""\n
    (Step {first_step_no})\n\tSet the mixer speed to number two and
    \tclose the guard and set the timer for {time} minutes.
    \tPress start.""")
    input("\n\tPress enter to move onto next step \n")

    print(f"""\n
    (Step {first_step_no + 1})\n\tOnce timer has finished and mixer
    \thas stopped. Open the guard and use the spatula 
    \tto scrape the mixture on the sides down into the bottom.""")
    input("\n\tPress enter to move onto next step \n")

    print(f"""\n
    (Step {first_step_no + 2})\n\tClose the guard, confirm the speed is
    \tfixed to 2 and set the timer for {time} minutes.
    \tPress start.""")
    input("\n\tPress enter to move onto next step \n")


def get_data():
    batch_data = SHEET.worksheet("batches")

    headers = batch_data.row_values(1)
    print(headers)
    batch_parameters = SHEET.worksheet("batches")
    headers = batch_parameters.row_values(1)


def save_batch_data(data_list):
    """
    Saves batch data to the batches worksheet
    by adding the list data on a new row.
    """
    print("\n\tUpdating batch sheet")
    selected_worksheet = SHEET.worksheet("batches")
    selected_worksheet.append_row(data_list)
    print("\n\tBatch Data saved on the worksheet successfully.\n")
    print("\n\tP R O C E S S   F I N I S H E D")
    input("\tPress enter to return to main menu.\n")


def get_employee_list():
    """
    Returns a list of employees extracted from worksheet
    """
    employee_list = SHEET.worksheet("employees").col_values(2)
    employees = employee_list[1:]
    return employees


def display_batch_data(no_cookies, recipe_no):
    """Function generates a batch number based on the recipe and date.
    Gathers all the information available to a list
    all data genrated is displayed via print statements"""
    batch_parameters = []

    past_batches = SHEET.worksheet("batches").get_all_values()
    number_for_batch = str(len(past_batches)).rjust(3, '0')
    today = date.today()
    today_readable = today.strftime("%d/%m/%Y")
    batch_parameters.append(today_readable)

    cookie_data = COOKIE_PROTOCOL[recipe_no]
    recipe = cookie_data["name"]
    batch_parameters.append(recipe)
    
    batch_number = (
        cookie_data["abbreviation"]
        + "-" + today_readable[8:] + "-" + (number_for_batch))
    batch_parameters.append(batch_number)
    batch_parameters.append(no_cookies)

    print("\n\tB A T C H    I N F O R M A T I O N")
    print("\n\tDATA GENERATED")
    print(f"\tRecipe Name:\t{recipe}")
    print(f"\tRecipe Amount:\t{no_cookies}")
    print(f"\tDate:\t\t{today}")
    print(f"\tBatch Number:\t{batch_number}")

    return batch_parameters


def request_employee_data(batch_parameters):
    employee_list = get_employee_list()
    print("\n\n\tE M P L O Y E E    D A T A")
    
    while True:
        print("\tComplete data with the employee's initials listed below:")
        print(f"\t{', '.join(employee_list)}")
        scribe = input("\tEnter Scribe initials: \n")
        if validate_data(scribe, "availble employee initials", employee_list):
            employee_list.remove(scribe)
            batch_parameters.append(scribe)
            break
    
    while True:
        print("\tComplete data with the employee's initials listed below:")
        print(f"\t{', '.join(employee_list)}")
        operator = input("\tEnter Operator initials: \n")
        if validate_data(operator, "availble employee initials", employee_list):
            batch_parameters.append(operator)
            break

    return batch_parameters


def main():
    """
    Runs the terminal functions
    """
    terminal_action = start_menu()
    if terminal_action == "a":
        protocol_info = select_recipe()
        #protocol_info = (11, "1")
    #protocol_info = ("55", "1")
    #batch_data_2 = ['12/02/2023', 'Classic Cookies', 'cl-23-002', 'wm', 'es']
        batch_data_1 = display_batch_data(protocol_info[0], protocol_info[1])
        batch_data_2 = request_employee_data(batch_data_1)
        start_manufacturing(protocol_info)
        mix_ingredients(protocol_info)
        batch_data_3 = bake_and_store(protocol_info, batch_data_2)
        save_batch_data(batch_data_3)
        main()


main()


#batch_data_3 = ['12/02/2023', 'Classic Cookies', 'cl-23-002', '11', 'es', 'lb', '11', '0', 'yes']
#save_batch_data(batch_data_3)
