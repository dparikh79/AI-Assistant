import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import API_ENDPOINT, API_KEY, PROMPT
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
                [{"role": "system", "content": PROMPT + relevant_passage}]
        }

        response = requests.post(API_ENDPOINT, headers=headers, json=data)

        try:
            return response.json()["choices"][0]["message"]["content"]
        except:
            print(response.json())