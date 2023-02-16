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

# Script for the Cookie Factory Terminal starts from here


def start_menu():
    """
    Function prints out the main menu presenting the user the
    available activities
    """
    print("\tC O O K I E   F A C T O R Y   H O M E  M E N U")
    print("\n\tWelcome to the Cookie Factory's procedure terminal!")
    print("\tAvailable actions:")
    print("\t\t a.	Bake Cookies")
    print("\t\t b.	View Batches")

    while True:
        choice = input("\n\tSelect an action by entering a or b:\n\t")
        if validate_data(choice, "a or b", ["a", "b"]):
            os.system('clear')
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
        raise ValueError
    except ValueError:
        print(f"\tINVALID DATA! Please enter {answer_string}.\n")
        return False


def validate_range(data, min_no, max_no):
    """Validates a data that should be within certain range"""
    try:
        if ((int(data) or data == "0") and
                int(data) in range(min_no, max_no + 1)):
            return True
        raise ValueError
    except ValueError:
        print(f"\n\tINVALID DATA! Please enter value from {min_no}-{max_no}.")
        return False


def view_batches():
    """
    Displays a menu for vieweing batches.
    presents two options: view by month or view last 5.
    User input is validated
    """
    print("\n\tV I E W   B A T C H E S")
    print("\n\tBatches from follwing timelines can be viewed:")
    print("\t\t a.	Spesific Month")
    print("\t\t b.	Last Five")

    while True:
        choice = input("\n\tPlease enter the choice by typing a or b: \n")
        if validate_data(choice, "a or c", ["a", "b"]):
            return choice


def request_month():
    """
    Requestss user input for year and month that user wishes to view.
    Validates input and formats year for get_months_batches
    """
    print("\n\tV I E W   B Y   M O N T H\n")
    this_year = date.today().year
    while True:
        year_choice = input("\tEnter the year(4 digits): \n")
        if validate_range(year_choice, 2022, this_year):
            break
    while True:
        month_choice = input("\tEnter the month number: \n")
        if validate_range(month_choice, 1, 12):
            month_int = int(month_choice)
            month_string = "0" + str(month_int) + "/" + year_choice
            print(f"Looking for: {month_string}")
            return month_string


def get_months_batches(time_frame):
    """
    Checks if any of the batches fit the given time_frame.
    Time-frame is month and year like 02/2023.
    All batches that fit the timeframe are printed.
    """
    header = SHEET.worksheet("batches").row_values(1)
    batches_data = SHEET.worksheet("batches").get_all_values()[1:]
    target_batches = []

    for batch in batches_data:
        if batch[0][3:] == time_frame:
            target_batches.append(batch)

    if not target_batches:
        print("\n\tNo batches were prepared on the selected month")
    else:
        for batch in target_batches:
            for i in range(9):
                print(f"\t{header[i].ljust(20)}-\t{batch[i]}")
            print("\n")
    while True:
        print("\n\tType 'view' to retunrn View Batches menu")
        choice = input("\tand 'main' to return to the Main Menu: \n")
        if validate_data(choice, 'view or main', ['view', 'main']):
            if choice == 'view':
                os.system('clear')
                view_batches()
            if choice == 'main':
                os.system('clear')
                main()


def last_five():
    """
    Prints out the last five batches.
    """
    header = SHEET.worksheet("batches").row_values(1)
    batches_data = SHEET.worksheet("batches").get_all_values()[-5:]
    print("\n\tV I E W   L A S T   5   B A T C H E S\n")

    for batch in batches_data:
        for i in range(9):
            print(f"\t{header[i].ljust(20)}-\t{batch[i]}")
        print("\n")
    while True:
        print("Type 'view' to retunrn View Batches menu")
        choice = input("and 'main' to return to the Main Menu: \n")
        if validate_data(choice, 'view or main', ['view', 'main']):
            if choice == 'view':
                os.system('clear')
                view_batches()
            if choice == 'main':
                os.system('clear')
                main()


def select_recipe():
    """
    Displays all available recipes and expect user input.
    User input is validated by running user input trhough validate_data
    function.
    """
    print("R E C I P E S    A V A I L A B L E\n")
    print("\tcl - Classic Cookies")
    print("\trw - Raspberry and White Chocolate Cookies")
    print("\tpb -  Peanut Butter Cookies")
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
            "\nHow many cookies you plan to prepare min 10 max 100: \n\t")
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
                print(
                    f"\n\t{ingredient_formatted}{total_weight * float(i[2])}g")
            else:
                print(f"\n\t {i[1]}")


def valid_made(max_value):
    """
    Validates the made cookies amount. Can'texceed the planned amount.
    Returns the user input after succesful validation.
    """
    while True:
        c_made = input("\n\tEnter the amount of cookies prepared:\n\t")
        if validate_range(c_made, 0, int(max_value)):
            print("\tData valid! Please proceed!")
            return c_made


def valid_dis(c_made, batch_object):
    """
    Validates the discarded cookies amount entered.
    If cookies made and discarded is the same run
    exit_early function is ran.
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
    If yes exit program early and runs the method save_batch from class
    Cookie_Batch
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
    Lists the label info for the process
    Requires instance created to displaying the correct info.
    """
    print(f"\n\tBatch Number:\t\t{batch_object.batch_no()}")
    print(f"\tType: \t\t\t{batch_object.name}")
    print(f"\tManufacturing date: \t{batch_object.batch_date}")


class CookieBatch:
    """
    Creates an instace of a batch.
    Includes methods for creating a batch number and
    saving batch data to the spreadsheet.
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
    Retrieves instruction data from worksheet "Instructions".
    Prints out intruction data unless key_word is encountered.
    A function or special statement is run. Returns a list of batch
    information: cookies_made, cookies_discarded, boolean that states
    if labelling took place.
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


def main():
    """
    Runs the terminal functions
    """
    main_menu_choice = start_menu()

    if main_menu_choice == 'a':
        view_choice = view_batches()
        if view_choice == "a":
            time_frame = request_month()
            get_months_batches(time_frame)
        if view_choice == "b":
            last_five()

    if main_menu_choice == "b":
        recipe_name, recipe_id, cookie_no = select_recipe()
        scribe, operator = input_employees()
        batch_date = generate_date()

        created_batch = CookieBatch(
            batch_date, recipe_name, recipe_id, cookie_no, scribe, operator)
        post_data = run_instructions(created_batch)
        created_batch.save_batch(created_batch.batch_no(), post_data)
        main()


main()
