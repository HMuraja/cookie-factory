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


class Instruction:
    def __init__(self, description):
        self.description = description


class Ingredient:
    def __init__(self, group_type, name, amount):
        self.group_type = group_type
        self.name = name
        self.amount = amount


class Recipe:
    def __init__(self, recipe_name, ingredient_list, instruction_list):
        self.recipe_name = recipe_name
        self.ingredient_list = ingredient_list
        self.instruction_list = instruction_list


class Batch:
    def __init__(self, amount, recipe):
        self.amount = amount
        self.recipe = recipe

# creating person class object
cookie_input = input("Please enter cookie type:")
cookie_no_input = input("How many you would like to make:")

step_data = (SHEET.worksheet("Instructions").get_all_values())[1:]
all_steps = []
for step in step_data:
    all_steps.append(Instruction(step))



all_ingredients = []
ingredient_data = (
    SHEET.worksheet(f"{cookie_input} ingredients").get_all_values())[1:]
for data in ingredient_data:
    all_ingredients.append(Ingredient(data[0], data[1], data[2]))

recipe_cookie = Recipe(cookie_input, all_ingredients, all_steps)


created_batch = Batch(cookie_no_input, recipe_cookie)
# create inner class object

for step in created_batch.recipe.
