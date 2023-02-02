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

print(RASPBERRY_WHITECHOCOLATE_COOKIE)

batches = SHEET.worksheet('batches')

batch_data = batches.get_all_values()

