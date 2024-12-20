from sentence_transformers import SentenceTransformer
import torch
from typing import List


class SentTransformer:
    def __init__(self, model_name: str):
        try:
            self.model = SentenceTransformer(model_name)
            print(f'Loaded SentenceTransformer model: {model_name}')
        except Exception as e:
            print(f'Failed to load SentenceTransformer model: {str(e)}')
            
    def get_similarity(self, text1: str, text2: str) -> float:
        '''计算两个文本之间的语义相似度'''
        embeddings1 = self.model.encode([text1])
        embeddings2 = self.model.encode([text2])
        return torch.nn.functional.cosine_similarity(
            torch.tensor(embeddings1), 
            torch.tensor(embeddings2)
        ).item()
    
    def find_most_similar(self, text: str, candidates: List[str]) -> str:
        '''找到候选列表中与输入文本最相似的项'''
        similarities = [self.get_similarity(text, c) for c in candidates]
        # from pprint import pprint; pprint([(text, c, self.get_similarity(text, c)) for c in candidates])
        return candidates[torch.argmax(torch.tensor(similarities))], max(similarities)
