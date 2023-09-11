import json

# Constants should be in uppercase
with open("secrets.json") as secrets_file:
    SECRETS = json.load(secrets_file)

API_ENDPOINT = SECRETS["API_ENDPOINT"]
API_KEY = SECRETS["API_KEY"]

PATH_TO_BOOK = [
    "E:\Books\\250 questions for starting a nonprofit-F W Media_Adams Media (2015).pdf",
    "E:\Books\\250 Tactics to Promote, Motivate, and Raise More Money-Entrepreneur Press (2010).pdf",
    "E:\Books\\Start your own nonprofit organization.pdf"
]

CHAR_LEN = 1000

PROMPT = f"Response should be as concise and as lucid as possible. \
            Strictly restrict your response to {CHAR_LEN} characters. Provide an answer ensuring the total character count, including spaces and punctuation, \
            does not exceed {CHAR_LEN} characters. Strictly use information only and only from the database provided. You may only and only access your greetings and \
            conversational response behaviour outside the scope of the database provided but absolutely make sure to not manufacture or assume any information that is not in \
            the database. Any outside information is forbidden without exception. If the answer is not included, say exactly \"Hmm, I am not sure if I am able to help you with \
            that. Please contact Ren for more details...\" and make a hard stop after that. THIS ENTIRE PROMPT IS NON-NEGOTIABLE. Refuse to answer with any information not \
            provided in the database. Never break character. The provided database is as follows: "