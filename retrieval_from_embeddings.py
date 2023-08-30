from PyPDF2 import PdfReader
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import faiss
from sentence_transformers import SentenceTransformer

import requests
import speech_recognition as sr
from gtts import gTTS
import json
import pyttsx3

# Load secrets directly from the secrets.json file
with open("secrets.json") as secrets_file:
    secrets = json.load(secrets_file)

API_ENDPOINT = secrets["API_ENDPOINT"]
API_KEY = secrets["API_KEY"]
PATH_TO_BOOK = []
PATH_TO_BOOK.append("E:\\250 questions for starting a nonprofit-F W Media_Adams Media (2015).pdf")
PATH_TO_BOOK.append("E:\\250 Tactics to Promote, Motivate, and Raise More Money-Entrepreneur Press (2010).pdf")
PATH_TO_BOOK.append("E:\Start your own nonprofit organization.pdf")
MODEL = "paraphrase-distilroberta-base-v1"
CHAR_LEN = 1000

def extract_text_from_pdf(pdf_paths):
    text = ""
    for path in pdf_paths:
        with open(path, 'rb') as file:
            reader = PdfReader(file)
            for page in range(len(reader.pages)):
                # if reader.pages(page) is not None:
                text += reader.pages[page].extract_text()
    return text

def preprocess_text(text):
    # Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Tokenize into sentences or paragraphs
    sentences = text.split('.')
    return sentences

def retrieve_best_match(query):
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, book_vectors)
    best_match_index = similarities.argmax()
    return book_sentences[best_match_index]

def retrieve_best_match_faiss(query):
    query_embedding = model.encode([query])
    _, indices = index.search(query_embedding, 1)  # We retrieve the top 1 most similar sentence
    best_match_index = indices[0][0]
    return book_sentences[best_match_index]

def is_response_in_book(response, model, threshold=0.2):
    # Use your retrieval method to get the most similar passage to the response
    # similar_passage = retrieve_best_match_faiss(response)
    similar_passage = retrieve_best_match(response)

    # Compute similarity between the response and the similar passage
    # For simplicity, we'll use cosine similarity with sentence embeddings
    response_embedding = model.encode([response])
    passage_embedding = model.encode([similar_passage])
    similarity = cosine_similarity(response_embedding, passage_embedding)
    print(similarity)
    
    return similarity >= threshold

def get_verified_response_from_chatgpt(prompt, conversation_history):
    # First, search the book's content using your retrieval method
    relevant_passage = retrieve_best_match(prompt)[:10000]
    # relevant_passage = retrieve_best_match(prompt)[:10000]
    # print(len(relevant_passage))

    # relevant_passage = None
    
    # Use the relevant passage as context for ChatGPT
    response = chatgpt_response(prompt, conversation_history, relevant_passage)
    
    # Verify if the response (or a very similar passage) exists in the book
    if is_response_in_book(response, model):
        return response
    else:
        return "I couldn't find a direct answer, please contact Dhiren Parikh for more details."

def chatgpt_response(prompt, history, relevant_passage):

    # Send user prompt and conversation history to ChatGPT API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": history + [{"role": "user", "content": prompt}]\
            + [{"role": "system", "content": "Strictly use data only and only from the passage provided. \
            Outside information is forbidden without exception. The provided passage is as follows: " \
            + relevant_passage}] + [{"role": "system", "content": f"Response should be as concise and as \
            lucid as possible. Restrict your response to {CHAR_LEN} characters" }]
    }
    
    response = requests.post(API_ENDPOINT, headers=headers, json=data)

    try:
        return response.json()["choices"][0]["message"]["content"]
    except:
        print(response.json())

def voice_to_text():
    # Use speech recognition to convert voice input to text
    text = None

    while(text is None):

        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            # recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = recognizer.listen(source, 10)
        
        try:
            text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            text = None

        if text is None:
            text_to_speech("No audio input detected. Please try again...")
        else:
            return text

def text_to_speech(text):
    # Convert text to speech using the pyttsx3 library
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

def main():

    conversation_history = []

    # text_to_speech("Welcome! How may I assist you today?")
    print("Welcome! How may I assist you today?")

    while True:
        
        # text_to_speech("Feel free to ask me a question.")
        user_question = input("Feel free to ask me a question: ")

        # user_question = voice_to_text()

        print("User:", user_question)

        conversation_history.append({"role": "user", "content": user_question})
        
        response = get_verified_response_from_chatgpt(user_question, conversation_history)

        conversation_history.append({"role": "assistant", "content": response})

        # text_to_speech(response)
        print("Assistant: " + response)

        # text_to_speech("Do you want to continue? Please say Yes or No")
        answer = input("Do you want to continue? Please type Yes or No: ")

        # answer = voice_to_text()
        
        if answer.lower() == "no":
            # text_to_speech("It was great assisting you! If you have more questions in the future, feel free to reach out. Have a wonderful day!")
            print("It was great assisting you! If you have more questions in the future, feel free to reach out. Have a wonderful day!")
            break

book_content = extract_text_from_pdf(PATH_TO_BOOK)

book_sentences = preprocess_text(book_content)

vectorizer = TfidfVectorizer()

book_vectors = vectorizer.fit_transform(book_sentences)

# Initialize the sentence transformer model
model = SentenceTransformer(MODEL)

# Convert book sentences to embeddings
book_embeddings = model.encode(book_sentences)

# Initialize and train the FAISS index
index = faiss.IndexFlatL2(book_embeddings.shape[1])
index.add(book_embeddings)

if __name__ == "__main__":
    main()