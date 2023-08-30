import pyttsx3
import speech_recognition as sr
import logging

logging.basicConfig(level=logging.INFO)

class AudioProcessor:
    @staticmethod
    def voice_to_text():
        text = None
        while text is None:
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()

                # # Adjust for ambient noise
                # recognizer.adjust_for_ambient_noise(source, duration=5)

                print("Listening...")
                try:
                    audio = recognizer.listen(source, timeout=10)
                    text = recognizer.recognize_google(audio)
                    return text
                except sr.UnknownValueError:
                    AudioProcessor.text_to_speech("Sorry, I couldn't understand the audio. Please try again...")
                except sr.WaitTimeoutError:
                    AudioProcessor.text_to_speech("No audio input detected within the timeout period. Please try again...")
                except sr.RequestError:
                    AudioProcessor.text_to_speech("There seems to be an issue with the internet connection. Please check and try again...")

    # def voice_to_text():
    #     recognizer = sr.Recognizer()
    #     retry_limit = 3
    #     retry_count = 0
        
    #     while retry_count < retry_limit:
    #         with sr.Microphone() as source:
    #             print("Listening...")
                
    #             # Adjust for ambient noise
    #             recognizer.adjust_for_ambient_noise(source, duration=5)
                
    #             try:
    #                 audio = recognizer.listen(source, timeout=10)
    #                 text = recognizer.recognize_google(audio)
    #                 return text
    #             except sr.UnknownValueError:
    #                 retry_count += 1
    #                 if retry_count < retry_limit:
    #                     AudioProcessor.text_to_speech("Sorry, I couldn't understand the audio. Please try again...")
    #                 else:
    #                     AudioProcessor.text_to_speech("Multiple attempts failed. Please check your microphone and surroundings and try again later.")
    #                     return None
    #             except sr.WaitTimeoutError:
    #                 retry_count += 1
    #                 if retry_count < retry_limit:
    #                     AudioProcessor.text_to_speech("No audio input detected within the timeout period. Please try again...")
    #                 else:
    #                     AudioProcessor.text_to_speech("Multiple attempts with no audio detected. Please check your microphone and try again later.")
    #                     return None
    #             except sr.RequestError:
    #                 AudioProcessor.text_to_speech("There seems to be an issue with the internet connection. Please check and try again...")
    #                 return None
    #             except Exception as e:
    #                 AudioProcessor.text_to_speech(f"An unexpected error occurred: {str(e)}. Please try again later.")
    #                 return None

    @staticmethod
    def text_to_speech(text):
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()