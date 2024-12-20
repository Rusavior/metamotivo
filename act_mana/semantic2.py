from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

class SentTfidf:
    def __init__(self):
        pass
            
    def find_most_similar(self, text: str, candidates: List[str]) -> str:
        '''找到候选列表中与输入文本最相似的项'''
        vectorizer = TfidfVectorizer().fit_transform([text] + candidates)
        vectors = vectorizer.toarray()
        cosine_matrix = cosine_similarity(vectors)
        similarities = cosine_matrix[0][1:]
        most_similar_index = similarities.argmax()
        return candidates[most_similar_index],  max(similarities)
