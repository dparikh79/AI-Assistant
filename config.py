import json

# Constants should be in uppercase
with open("secrets.json") as secrets_file:
    SECRETS = json.load(secrets_file)

API_ENDPOINT = SECRETS["API_ENDPOINT"]
API_KEY = SECRETS["API_KEY"]

PATH_TO_BOOK = [
    "E:\\250 questions for starting a nonprofit-F W Media_Adams Media (2015).pdf",
    "E:\\250 Tactics to Promote, Motivate, and Raise More Money-Entrepreneur Press (2010).pdf",
    "E:\\Start your own nonprofit organization.pdf"
]

# PATH_TO_BOOK = [
#     input("Please provide the path to the first book: "),
#     input("Please provide the path to the second book: "),
#     input("Please provide the path to the third book: ")
# ]

MODEL = "paraphrase-distilroberta-base-v1"
CHAR_LEN = 1000
