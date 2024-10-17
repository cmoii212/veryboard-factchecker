from sentence_transformers import util

class RelevanceFilter:
    def __init__(self, model):
        self.model = model

    def extract_relevant_passages(self, claim, text, top_k=7):
        # Split text into sentences or passages
        passages = text.split('. ')
        # Compute similarity scores
        scores = []
        for passage in passages:
            score = self.compute_similarity(claim, passage)
            scores.append((passage, score))
        # Sort and select top_k passages
        sorted_passages = sorted(scores, key=lambda x: x[1], reverse=True)
        top_passages = [p[0] for p in sorted_passages[:top_k]]
        return ' '.join(top_passages)

    def compute_similarity(self, text1, text2):
        embeddings1 = self.model.encode(text1, convert_to_tensor=True)
        embeddings2 = self.model.encode(text2, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)
        return cosine_scores.item()
