from config import PATH_TO_BOOK, MODEL
from pdf_processor import PDFProcessor
from chatbot import Chatbot
from audio_processor import AudioProcessor
import logging

logging.basicConfig(level=logging.INFO)

class Assistant:
    def __init__(self, paths, model_name):
        self.paths = paths
        self.model_name = model_name
        self.processor = PDFProcessor(self.paths)
        self.book_content = self.processor.extract_text_from_pdf()
        self.book_sentences = self.processor.preprocess_text(self.book_content)
        self.chatbot = Chatbot(self.book_sentences)

    def main(self):
        conversation_history = []
        # text_to_speech("Welcome! How may I assist you today?")
        logging.info("Welcome! How may I assist you today?")
        while True:
            # AudioProcessor.text_to_speech("Feel free to ask me a question.")
            user_question = input("Feel free to ask me a question: ")

            # user_question = AudioProcessor.voice_to_text()
            logging.info(f"User: {user_question}")

            conversation_history.append({"role": "user", "content": user_question})
            response = self.chatbot.get_verified_response_from_chatgpt(user_question, conversation_history)
            conversation_history.append({"role": "assistant", "content": response})

            # AudioProcessor.text_to_speech(response)
            logging.info(f"Assistant: {response}")
            
            # AudioProcessor.text_to_speech("Do you want to continue? Please say Yes or No")
            answer = input("Do you want to continue? Please type Yes or No: ")
            
            # answer = AudioProcessor.voice_to_text()

            if answer.lower() == "no":
                # AudioProcessor.text_to_speech("It was great assisting you! If you have more questions in the future, feel free to reach out. Have a wonderful day!")
                logging.info("It was great assisting you! If you have more questions in the future, feel free to reach out. Have a wonderful day!")
                break

if __name__ == "__main__":
    assistant = Assistant(PATH_TO_BOOK, MODEL)
    assistant.main()
