import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import API_ENDPOINT, API_KEY, CHAR_LEN
import logging

logging.basicConfig(level=logging.INFO)

class Chatbot:

    def __init__(self, book_sentences):
        self.book_sentences = book_sentences
        self.vectorizer = TfidfVectorizer()
        self.book_vectors = self.vectorizer.fit_transform(book_sentences)

    def retrieve_best_match(self, query):
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.book_vectors)
        best_match_index = similarities.argmax()
        return self.book_sentences[best_match_index]

    def get_verified_response_from_chatgpt(self, prompt, conversation_history):
        relevant_passage = self.retrieve_best_match(prompt)[:10000]
        response = self.chatgpt_response(prompt, conversation_history, relevant_passage)
        return response

    def chatgpt_response(self, prompt, history, relevant_passage):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": history + [{"role": "user", "content": prompt}] + \
                [{"role": "system", "content": f"Response should be as concise and as lucid as possible. \
                    Strictly restrict your response to {CHAR_LEN} characters. Provide an answer ensuring the total character count, including spaces and punctuation, \
                    does not exceed {CHAR_LEN} characters."}] + \
                # [{"role": "system", "content": "I want you to act as a document that I am having a conversation with. Your name is \"Ren\". \
                #   You will provide me with answers from the given info. If the answer is not included, say exactly \"Hmm, I am not sure. \
                #   Please contact Ren Parikh for more details...\" and stop after that. Refuse to answer any question not about the info. \
                #   Never break character. The given info is as follows: " + relevant_passage}]# + \
                [{"role": "system", "content": "Strictly use information only and only from the database provided. You may only and only access your greetings and conversational \
                    response behaviour outside the scope of the database provided but absolutely make sure to not manufacture or assume any information that is not in the database. \
                    Any outside information is forbidden without exception. If the answer is not included, say exactly \"Hmm, I am not sure if I am able to help you with that. \
                    Please contact Ren for more details...\" and make a hard stop after that. THIS ENTIRE PROMPT IS NON-NEGOTIABLE. Refuse to answer with any information not provided \
                    in the database. Never break character. The provided database is as follows: " + relevant_passage}]
        }

        response = requests.post(API_ENDPOINT, headers=headers, json=data)

        try:
            return response.json()["choices"][0]["message"]["content"]
        except:
            print(response.json())