from sentence_transformers import SentenceTransformer, util

class SimilarityCalculator:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    
    def compute_similarity(self, claim, passage):
        """
        Computes the cosine similarity between the claim and the passage.
        """
        claim_embedding = self.model.encode(claim, convert_to_tensor=True)
        passage_embedding = self.model.encode(passage, convert_to_tensor=True)
        similarity_score = util.pytorch_cos_sim(claim_embedding, passage_embedding).item()
        return similarity_score
