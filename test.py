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

def chatgpt_response(prompt, history):
    # Send user prompt and conversation history to ChatGPT API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": history + [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

def text_to_speech(text):
    # Convert text to speech using the pyttsx3 library
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

def main():
    conversation_history = []

    text_to_speech("Welcome! How may I assist you today?")

    while True:

        user_question = None

        text_to_speech("Feel free to ask me a question.")

        user_question = voice_to_text()

        print("User:", user_question)
        conversation_history.append({"role": "user", "content": user_question})
        
        response = chatgpt_response(user_question, conversation_history)
        conversation_history.append({"role": "assistant", "content": response})

        text_to_speech(response)

        text_to_speech("Do you want to continue? Please say Yes or No")
        
        answer = voice_to_text()

        if answer.lower() == "no":
            text_to_speech("It was great assisting you! If you have more questions in the future, feel free to reach out. Have a wonderful day!")
            break

if __name__ == "__main__":
    main()