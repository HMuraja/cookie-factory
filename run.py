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

# Set up APIs
batches = SHEET.worksheet('batches')
batch_data = batches.get_all_values()

# Script for the Cookie Factory Terminal starts from here

def start_menu():
    """
    Function prints out the main menu presenting the user the
    available activities
    """
    print("C O O K I E   F A C T O R Y   H O M E  M E N U")
    print("\nWelcome to the Cookie Factory's procedure terminal!")
    print("Available actions:")
    print("\t a.	Bake Cookies")
    print("\t b.	View Batches")

    while True:
        choice = input("\nSelect an action by entering a or b:\n\t")
        if validate_data(choice, "a or b", ["a", "b"]):
            if choice == "a":
                os.system('clear')
            else:
                print("Uploading batch data...(Batches Code not buld yet)\n")
            break
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
        print(f"\tINVALID DATA!{error}, please try again.\n")
        return False


def validate_range(data, min_no, max_no):
    """Validates a data that should be within certain range"""
    try:
        if ((int(data) or data == "0") and
                int(data) in range(min_no, max_no + 1)):
            return True
        raise ValueError
    except ValueError:
        print(f"""\n\tINVALID DATA!
        Please enter {min_no}-{max_no}, please try again.""")
        return False


def select_recipe():
    """
    Displays all available recipes and expect user input.
    User input is validated by running user input trhough validate_data
    function.
    """
    print("P R O T O C O L S   A V A I L A B L E")
    print("\nAvailable recipes:")
    print("\t1.	Classic Cookies")
    print("\t2.	Raspberry and White Chocolate Cookies")
    print("\t3.	Peanut Butter Cookies")
    while True:
        print("\nPlease select a recipe.")
        recipe_choice = input("Enter the corresponding number: \n\t")
        if validate_data(recipe_choice, "1, 2 or 3", ['1', '2', '3']):
            break
    while True:
        amount = input(
            "\nHow many cookies you plan to prepare min 10 max 100): \n\t")
        if validate_range(amount, 10, 100):
            os.system('clear')
            return (recipe_choice, amount)


def generate_date():
    """
    Generates today's date.
    """
    today = date.today().today.strftime("%d/%m/%Y")
    return today


def generate_batch_number(recipe_no, date_string):
    """
    Function generates a batch number based on the recipe and date.
    Gathers all the information available to a list
    all data genrated is displayed via print statements
    """
    past_batches = SHEET.worksheet("batches").get_all_values()
    number_for_batch = str(len(past_batches)).rjust(3, '0')

    cookie_data = COOKIE_PROTOCOL[recipe_no]
    batch_number = (
        cookie_data["abbreviation"]
        + "-" + date_string[8:] + "-" + (number_for_batch))
    return batch_number


def get_employee_list():
    """
    Returns a list of employees extracted from worksheet
    """
    employee_list = SHEET.worksheet("employees").col_values(2)
    employees = employee_list[1:]
    return employees


def request_employee_data(batch_parameters):
    """
    Requests user to enter employee initials for requested role.
    Runs validation for the enteres information.
    If valid data appended to batch_parameters list which is returned.
    """
    employee_list = get_employee_list()
    print("\n\n\tEMPLOYEE DATA")
    while True:
        print("\tComplete data with the employee's initials listed")
        print(f"\n\tAvailable Employees: {', '.join(employee_list)}")
        scribe = input("\tEnter Scribe initials: \n\t")
        if validate_data(scribe, "availble employee initials", employee_list):
            employee_list.remove(scribe)
            batch_parameters.append(scribe)
            break
    while True:
        print(f"\n\tAvailable Employees: {', '.join(employee_list)}")
        operator = input("\tEnter Operator initials: \n\t")
        if validate_data(
                operator, "available employee initials", employee_list):
            batch_parameters.append(operator)
            input("\n\tPress ENTER when ready to run the instructions")
            os.system('clear')
            break

    return batch_parameters


def list_ingredients(batch_info, ingredient_list, add_weight):
    """
    List ingredients from start to finish
    """

    recipe = COOKIE_PROTOCOL[batch_info[1]]
    total_weight = 90 * int(batch_info[0])
    list_items = recipe[ingredient_list]

    for ingredient in list_items.keys():
        ingredient_weight = total_weight * list_items[ingredient]
        ingredient_formatted = ingredient.ljust(20)
        if add_weight == "yes":
            print(f"\n\t {ingredient_formatted}{ingredient_weight}g")
        else:
            print(f"\n\t {ingredient}")


def valid_made(batch_info):
    """
    Validates the made cookies amount.
    """
    recipe_amount = batch_info[3]
    while True:
        c_made = input("\n\tEnter the amount of cookies prepared:\n\t")
        if validate_range(c_made, 0, int(recipe_amount)):
            print("\tData valid! Please proceed!")
            batch_info.extend([c_made])
            break


def valid_dis(batch_info):
    """
    Validates the discarded cookies amount entered.
    If cookies made and discarded is the same run the program ends.
    """
    c_made = batch_info[6]

    while True:
        c_disc = input("\n\tEnter the amount of cookies discarded:\n\t")
        if validate_range(c_disc, 0, int(c_made)):
            if c_disc == c_made:
                exit_early(batch_info)
            else:
                batch_info.extend([c_disc])
                print("\n\tData valid! Please proceed!")
                break


def exit_early(batch_info):
    """
    Confirm if entered cookie number was 0.
    If yes exit program early.
    """
    while True:
        choice = input("\n\tAll cookies dicarded? Type yes or no: \n\t")
        if validate_data(choice, "yes or no", ["yes", "no"]):
            if choice == "yes":
                batch_info.extend([batch_info[6], "no"])
                save_batch_data(batch_info)
                main()
            break


def label_info(batch_info):
    """
    Lists the label infor for the process
    Requires batch info for displaying the correct info
    """
    print(f"\n\tBatch Number:\t\t{batch_info[2]}")
    print(f"\tType: \t\t\t{batch_info[1]}")
    print(f"\tManufacturing date: \t{batch_info[0]}")


def run_instructions(recipe_input, batch_info):
    """
    Prints out instructions from procedure dictionary
    """
    weight = int(recipe_input[1]) * 90
    recipe_no = recipe_input[1]
    recipe_details = COOKIE_PROTOCOL[recipe_no]
    title = (recipe_details["name"]).upper()

    print(f"\n\tR U N N I N G   R E C I P E:\n\t{title}")

    for no in PROCEDURE_STEPS:
        instructions = PROCEDURE_STEPS[no]
        print(f"\n(Step {no})")
        for i in instructions:
            if i == "list_all":
                list_ingredients(recipe_input, "wet ingredients", "no")
                list_ingredients(recipe_input, "dry ingredients", "no")
            elif i == "list_w_i":
                list_ingredients(recipe_input, "wet ingredients", "yes")
            elif i == "list_d_i":
                list_ingredients(recipe_input, "dry ingredients", "yes")
            elif i == "tray no":
                tray_no = math.ceil(weight/90/10)
                print(f"\tPlace {tray_no} tray on the work surface.")
            elif i == "made input":
                valid_made(batch_info)
            elif i == "discarded input":
                valid_dis(batch_info)
            elif i == "label info":
                label_info(batch_info)
            else:
                print(f"\n\t{i}")
        input("\n\tPress ENTER to move onto next step \n\t")
        os.system('clear')
    batch_info.append("yes")
    return batch_info


def save_batch_data(data_list):
    """
    Saves batch data to the batches worksheet
    by adding the list data on a new row.
    """
    print("\n\tU P D A T I N G   B A T C H   S H E E T")
    selected_worksheet = SHEET.worksheet("batches")
    selected_worksheet.append_row(data_list)
    print("\n\tBatch Data saved on the worksheet successfully.\n")
    print("\n\tP R O C E S S   F I N I S H E D")
    input("\tPress enter to return to main menu.\n\n")
    os.system('clear')


def main():
    """
    Runs the terminal functions
    """
    terminal_action = start_menu()
    if terminal_action == "a":
        recipe_no, cookie_no = select_recipe()
        todays_date = generate_date()
        batch_no = generate_batch_number(cookie_no, date)
    # protocol_info = ("55", "1")
    # batch_data_2 = ['12/02/2023', 'Classic Cookies', 'cl-23-002', 'wm', 'es']
        batch_i_1 = display_batch_data(
            cookie_recipe[0], cookie_recipe[1], todays_date)
        batch_i_2 = request_employee_data(batch_i_1)
        final_data = run_instructions(cookie_recipe, batch_i_2)
        save_batch_data(final_data)
        main()


main()

# list_ingredients(["1", "55"], "dry ingredients", "yes")