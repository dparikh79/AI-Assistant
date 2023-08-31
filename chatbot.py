import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import faiss
from sentence_transformers import SentenceTransformer
from config import API_ENDPOINT, API_KEY, MODEL, CHAR_LEN
import logging

logging.basicConfig(level=logging.INFO)

class Chatbot:

    def __init__(self, book_sentences):
        self.book_sentences = book_sentences
        self.vectorizer = TfidfVectorizer()
        self.book_vectors = self.vectorizer.fit_transform(book_sentences)
        self.model = SentenceTransformer(MODEL)
        self.book_embeddings = self.model.encode(book_sentences)
        self.index = faiss.IndexFlatL2(self.book_embeddings.shape[1])
        self.index.add(self.book_embeddings)

    def retrieve_best_match(self, query):
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.book_vectors)
        best_match_index = similarities.argmax()
        return self.book_sentences[best_match_index]

    def retrieve_best_match_faiss(self, query):
        query_embedding = self.model.encode([query])
        _, indices = self.index.search(query_embedding, 1)
        best_match_index = indices[0][0]
        return self.book_sentences[best_match_index]

    def is_response_in_book(self, response, threshold=0.2):
        similar_passage = self.retrieve_best_match(response)
        response_embedding = self.model.encode([response])
        passage_embedding = self.model.encode([similar_passage])
        similarity = cosine_similarity(response_embedding, passage_embedding)
        return similarity >= threshold

    def get_verified_response_from_chatgpt(self, prompt, conversation_history):
        relevant_passage = self.retrieve_best_match(prompt)[:10000]
        response = self.chatgpt_response(prompt, conversation_history, relevant_passage)
        if self.is_response_in_book(response):
            return response
        else:
            response = "I couldn't find a direct answer, please contact Dhiren Parikh for more details."
            return response

    def chatgpt_response(self, prompt, history, relevant_passage):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": history + [{"role": "user", "content": prompt}] + [{"role": "system", "content": "Strictly use data only and only from the passage provided. Outside information is forbidden without exception. The provided passage is as follows: " + relevant_passage}] + [{"role": "system", "content": f"Response should be as concise and as lucid as possible. Restrict your response to {CHAR_LEN} characters"}]
        }
        # print("c1")
        response = requests.post(API_ENDPOINT, headers=headers, json=data)
        # print("c2")
        try:
            return response.json()["choices"][0]["message"]["content"]
        except:
            print(response.json())