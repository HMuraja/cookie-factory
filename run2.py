from datetime import date
import os
import gspread
from google.oauth2.service_account import Credentials
import textwrap

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('cookie_batches')


def main_menu():
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
        raise ValueError
    except ValueError:
        print(f"\tINVALID DATA!\n\tPlease enter {answer_string}.")
        return False


def validate_range(data, min_no, max_no):
    """Validates a data that should be within certain range"""
    try:
        if ((int(data) or data == "0") and
                int(data) in range(min_no, max_no + 1)):
            return True
        raise ValueError
    except ValueError:
        print(f"\n\tINVALID DATA! Please enter {min_no}-{max_no}")
        return False


def select_recipe():
    """
    Displays all available recipes and expect user input.
    User input is validated by running user input trhough validate_data
    function.
    """
    print("R E C I P E S  A V A I L A B L E")
    print("\t1.	Classic Cookies")
    print("\t2.	Raspberry and White Chocolate Cookies")
    print("\t3.	Peanut Butter Cookies")
    while True:
        choice = input("\nPlease select a recipe by etering the corresponding number:\n")
        if validate_data(choice, "1, 2 or 3", ['1', '2', '3']):
            if choice == "1":
                recipe_name = "Classic Cookies"
                name_abr = "cl"
            elif choice == "2":
                recipe_name = "Raspberry and White Chocolate Cookies"
                name_abr = "rw"
            elif choice == "3":
                recipe_name = "Peanut Butter Cookies"
                name_abr = "pb"
            break
    while True:
        amount = input(
            "\nHow many cookies you plan to prepare min 10 max 100): \n\t")
        if validate_range(amount, 10, 100):
            os.system('clear')
            return (amount, recipe_name, name_abr)


def request_employee_data():
    """
    Requests user to enter employee initials for requested role.
    Runs validation for the enteres information.
    If valid data appended to batch_parameters list which is returned.
    """

    employee_list = SHEET.worksheet("employees").col_values(2)
    employees = employee_list[1:]
    print("\n\n\tE M P L O Y E E   D A T A")
    while True:
        print("\tAdd involved employee's initials after the role")
        print(f"\n\tAvailable Employees: {', '.join(employees)}")
        scribe = input("\tProcess scribe: \n\t")
        if validate_data(scribe, "availble employee initials", employees):
            employees.remove(scribe)
            break
    while True:
        print(f"\n\tAvailable Employees: {', '.join(employees)}")
        operator = input("\tProcess operator: \n\t")
        if validate_data(
                operator, "available employee initials", employees):
            input("\n\tPress ENTER when ready to run the instructions")
            os.system('clear')
            break

    return (scribe, operator)


def gen_date():
    """ 
    Generates a date.
    """
    today = date.today().strftime("%d/%m/%Y")
    return today


def main():
    """
    Runs the terminal functions
    """
    terminal_action = main_menu()
    if terminal_action == "a":
        process_date = gen_date()
        selected_amount, recipe_name, name_abr = select_recipe()
        selected_scribe, selected_operator = request_employee_data()
        batch = CookieBatch(
            process_date, selected_amount, recipe_name, name_abr, selected_scribe, selected_operator)
        print(batch)

#main()


class CookieBatch:
    """
    Creates an instace of a batch
    """
    batch_list = []
    
    def __init__(self, date, recipe, abr, amount, scribe, operator):
        self.date = date
        self.recipe = recipe
        self.abr = abr
        self.amount = amount
        self.scribe = scribe
        self.operator = operator

    def gen_batch_no(self):
        """
        Generates a batch number for the batch
        Uses "abr" name abreaviation, two last numbers of the year
        and generates a 3 digits number based on last batch entry
        """
        past_batches = SHEET.worksheet("batches").get_all_values()
        number_for_batch = str(len(past_batches)).rjust(3, '0')
        date_abr = self.date[8:] 
        batch_number = (
            self.abr + "-" + date_abr + "-" + (number_for_batch))
        return batch_number

    def get_ing_dict(self, ing_type):
        """
        Generates a ingredients dictionary for the object.
        Depending on ingredients type, will produce dictionary including only
        "wet" or "dry" ingredients.
        Key is ingredient and value is its's weight in grams.
        Ingredient data is extracted from the google spreadsheet.
        Each recipe has it's own worksheet in the spreadsheet..
        """
        list_row_values = SHEET.worksheet(
            f"{self.abr} Ingredients").get_all_values()
        ing_w_dict = {}

        for cell_value in list_row_values:
            if cell_value[0] == ing_type:
                ing_name = [cell_value[1]]
                ing_weight = cell_value(ing[2]) * 90 * self.amount
                # weight is a result of multiplying the ingredient ration
                # with individual cookie weight, "90g", and then multiplying  
                # this by the number of cookies, "amount".
                ing_w_dict[ing_name] = ing_weight
    


scoop_ins = "Place one scoop of cookie dough on the scale. Add or remove dough until it weights around 85-95g. Place the measured dough on the baking sheet. Repeat the process until dough is finished. IF the last cookie is less than 85 g, discard this dough."

instruction_list = (SHEET.worksheet("Instructions").get_all_values())[1:]

for step_no in range(len(instruction_list)):
    print(f"S T E P   {step_no + 1}")
    step_instructions = instruction_list[step_no]
    for instruction in step_instructions:
        if instruction == "list_all":
            print("listing")
        elif instruction == "list_w_i":
            print("listing")
        elif instruction == "list_d_i":
            print("listing")
        elif instruction == "tray no":
            tray_no = "x"
            print(f"\tPlace {tray_no} tray on the work surface.")
        elif instruction == "made input":
            print("validating")
        elif instruction == "discarded input":
            print("validating")
        elif instruction == "label info":
            print("validating")
        else:
            lines = textwrap.wrap(instruction, 72, break_long_words=False)
            for line in lines:
                print(f"\t{line}")
    input("\n\tPress ENTER to move onto next step \n\t")
    os.system('clear')
