# 79 79 79 79 79 79 79 -- MAX width of your terminal-- 79 79 79 79 79 79 79 79
# External libraries to access google sheets
import math
from datetime import date
import os
import textwrap
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
    print("R E C I P E S    A V A I L A B L E\n")
    print("\t Classic Cookies - rw")
    print("\t Raspberry and White Chocolate Cookies - rw")
    print("\t Peanut Butter Cookies - pb")
    while True:
        recipe_choice = input(
            "\n Select recipe by entereing cl, rw or pb:\n\t")
        if validate_data(recipe_choice, "cl, rw or pb", ['cl', 'rw', 'pb']):
            if recipe_choice == "cl":
                name = "Classic Cookie"
            if recipe_choice == "rw":
                name = "Raspberry White Chocolate Cookie"
            if recipe_choice == "pb":
                name = "Peanut Butter Cookie"
            break
    while True:
        amount = input(
            "\nHow many cookies you plan to prepare min 10 max 100): \n\t")
        if validate_range(amount, 10, 100):
            os.system('clear')
            return (name, recipe_choice, amount)


def input_employees():
    """
    Requests user to enter employee initials for requested role.
    Runs validation for the enteres information.
    List with initials added.
    """
    employee_list = (SHEET.worksheet("employees").col_values(2))[1:]
    employees = []
    roles = ["Scribe", "Operator"]
    print("\n\tE M P L O Y E E   D A T A")
    print("\n\tAdd involved employee's initials after the role")
    for role in roles:
        while True:
            print(f"\tAvailable Employees: {', '.join(employee_list)}")
            choice = input(f"\n\tProcess {role}: \n\t")
            if validate_data(choice, "listed employee initals", employee_list):
                employee_list.remove(choice)
                employees.append(choice)
                break
    input("\n\tPress ENTER when ready to run the instructions")
    os.system('clear')
    return employees


def generate_date():
    """
    Generates today's date.
    """
    today = date.today().strftime("%d/%m/%Y")
    return today


def generate_batch_no(abbreviation, date_string):
    """
    Function generates a batch number based on the recipe and date.
    Gathers all the information available to a list
    all data genrated is displayed via print statements
    """
    past_batches = SHEET.worksheet("batches").get_all_values()
    number_for_batch = str(len(past_batches)).rjust(3, '0')
    batch_number = (
        abbreviation + "-" + date_string[8:] + "-" + (number_for_batch))
    return batch_number


def list_ingredients(batch_object, ingredient_type, add_weight):
    """
    List ingredients from start to finish
    """
    ingredient_data = (SHEET.worksheet(batch_object.name).get_all_values())[1:]
    total_weight = int(batch_object.amount) * 90
    for i in ingredient_data:
        if ingredient_type in i:
            ingredient_formatted = (i[1]).ljust(20)
            if add_weight == "yes":
                print(f"\n\t{ingredient_formatted}{total_weight * float(i[2])}g")
            else:
                print(f"\n\t {i[1]}")


def valid_made(max_value):
    """
    Validates the made cookies amount.
    """
    while True:
        c_made = input("\n\tEnter the amount of cookies prepared:\n\t")
        if validate_range(c_made, 0, int(max_value)):
            print("\tData valid! Please proceed!")
            return c_made


def valid_dis(c_made, batch_object):
    """
    Validates the discarded cookies amount entered.
    If cookies made and discarded is the same run the program ends.
    """

    while True:
        c_disc = input("\n\tEnter the amount of cookies discarded:\n\t")
        if validate_range(c_disc, 0, int(c_made)):
            if c_disc == c_made:
                exit_early(batch_object, c_disc, c_made)
            else:
                return c_disc


def exit_early(batch_object, made, discarded):
    """
    Confirm if entered cookie number was 0.
    If yes exit program early.
    """
    while True:
        choice = input("\n\tAll cookies dicarded? Type yes or no: \n\t")
        if validate_data(choice, "yes or no", ["yes", "no"]):
            if choice == "yes":
                batch_no = batch_object.batch_no()
                post_data = [made, discarded, "no"]
                batch_object.save_batch(batch_no, post_data)
                main()
            break


def label_info(batch_object):
    """
    Lists the label infor for the process
    Requires batch info for displaying the correct info
    """
    print(f"\n\tBatch Number:\t\t{batch_object.batch_no()}")
    print(f"\tType: \t\t\t{batch_object.name}")
    print(f"\tManufacturing date: \t{batch_object.batch_date}")


class CookieBatch:
    """
    Creates an instace of a batch
    """
    def __init__(
            self, batch_date, name, recipe_abbreviation, amount, scribe,
            operator):
        self.batch_date = batch_date
        self.name = name
        self.recipe_abbreavion = recipe_abbreviation
        self.amount = amount
        self.scribe = scribe
        self.operator = operator

    def batch_no(self):
        """
        Generates batch number by joining recipe_abbreviation,
        manufacturing years two last numbers and the batch count.
        For example, for Classic Cookies, baked on 15/02/2023 and batch
        being 10th ever manufactured the batch number would be cl-23-010.
        """
        past_batches = SHEET.worksheet("batches").get_all_values()
        batch_count = str(len(past_batches)).rjust(3, '0')
        date_abr = self.batch_date[8:]
        batch_number = (
            self.recipe_abbreavion + "-" + date_abr + "-" + (batch_count))
        return batch_number
    
    def save_batch(self, batch_no, post_data):
        """
        Saves batch data to the batches worksheet
        by adding the final_list on a new row.
        """
        final_list = [
            self.batch_date, self.name, batch_no,
            self.amount, self.scribe, self.operator]
        for data in post_data:
            final_list.append(data)
        print("\n\tU P D A T I N G   B A T C H   S H E E T")
        selected_worksheet = SHEET.worksheet("batches")
        selected_worksheet.append_row(final_list)
        print("\n\tBatch Data saved on the worksheet successfully.\n")
        print("\n\tP R O C E S S   F I N I S H E D")
        input("\tPress enter to return to main menu.\n\n")
        os.system('clear')


def run_instructions(batch_object):
    """
    Prints out instructions from procedure dictionary
    """
    instruction_data = (SHEET.worksheet("Instructions").get_all_values())[1:]
    title = (batch_object.name).upper()

    for i in range(len(instruction_data)):
        print(f"\n\tR U N N I N G   R E C I P E:\n\t{title}")
        print(f"\n\tS T E P  {i + 1}.")
        for set in instruction_data[i]:
            if set == '':
                break
            elif set == "list_all":
                list_ingredients(batch_object, "wet", "no")
                list_ingredients(batch_object, "dry", "no")
            elif set == "list_w_i":
                list_ingredients(batch_object, "wet", "yes")
            elif set == "list_d_i":
                list_ingredients(batch_object, "dry", "yes")
            elif set == "tray no":
                tray_no = math.ceil(int(batch_object.amount)/10)
                print(f"\tPrepare {tray_no} tray(s)")
            elif set == "made input":
                cookies_made = valid_made(batch_object.amount)
            elif set == "discarded input":
                cookies_discarded = valid_dis(cookies_made, batch_object)
            elif set == "label info":
                label_info(batch_object)
            else:
                lines = textwrap.wrap(
                    set, 72, break_long_words=False)
                for line in lines:
                    print(f"\t{line}")
        input("\n\tPress ENTER to move onto next step \n\t")
        os.system('clear')
    return [cookies_made, cookies_discarded, "yes"]


# https://stackoverflow.com/questions/32122022/split-a-string-into-pieces-of-max-length-x-split-only-at-spaces 
# Code for splitting strings when over desired number but avoiding from splitting words


def main():
    """
    Runs the terminal functions
    """
    #terminal_action = start_menu()
    #if terminal_action == "a":
    recipe_name, recipe_id, cookie_no = ['Classic Cookie', 'cl', '20'] # select_recipe()
    scribe, operator = ['es', 'wb'] # input_employees()
    batch_date = generate_date()

    created_batch = CookieBatch(
        batch_date, recipe_name, recipe_id, cookie_no, scribe, operator)
    run_instructions(created_batch)
        #batch_i_1 = display_batch_data(
            #cookie_recipe[0], cookie_recipe[1], todays_date)
        #batch_i_2 = request_employee_data(batch_i_1)
        #final_data = run_instructions(cookie_recipe, batch_i_2)
        #save_batch_data(final_data)
       # main()


main()

# list_ingredients(["1", "55"], "dry ingredients", "yes")
