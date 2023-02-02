# Write your code to expect a terminal of 80 characters wide and 24 rows high__
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('cookie_batches')

"""The three available recipes are listed below as constant variables"""
RASPBERRY_WHITECHOCOLATE_COOKIE = {
    "wet ingredients": {
        "Butter": 0.16,
        "Vanilla Extract": 0.005,
        "Raspberries": 0.10, 
        "White Sugar": 0.16}, 
    "dry ingredients": {
        "Flour": 0.38,
        "Baking Powder": 0.003,
        "Baking Soda": 0.002,
        "White Chocolate": 0.19}}

CLASSIC_COOKIE = {
    "wet ingredients": {
        "Butter": 0.16,
        "Vanilla Extract": 0.005,
        "Egg Mix": 0.10,
        "Light Brown Sugar": 0.16},
    "dry ingredients": {
        "Flour": 0.38,
        "Baking Powder": 0.003,
        "Baking Soda": 0.002,
        "White Chocolate": 0.19}}

PEANUT_BUTTER_COOKIE = {
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
        "Reesee’s Chips": 0.19}}

batches = SHEET.worksheet('batches')

batch_data = batches.get_all_values()


def start_menu():
    """Function prints out the main menu where user can choose from
    displayed activities"""

    print("Welcome to the Cookie Factory’s procedure terminal!")
    print("Available actions:")
    print("\t a.	Bake Cookies")
    print("\t b.	View Batches")

    while True:
        choice = input("\nSelect an action by entering a or b:\n")
        if validate_data(choice):
            if choice == "a":
                print("\nUploading available Recipes...\n")
            else:
                print("\nUploading batch data...\n")
            break
    return choice


def validate_data(data):
    """
    Try, checks the entered data and 
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        if data != "a" and data != "b":
            raise ValueError(
                "Please enter either a or b"
            )
    except ValueError as e:
        print(f"\nInvalid data! {e}, please try again.")
        return False  
    return True


selection = start_menu()
