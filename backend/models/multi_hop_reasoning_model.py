# backend/models/multi_hop_reasoning_model.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class MultiHopReasoningModel:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # Specify use_fast=False to use the slow tokenizer compatible with SentencePiece
        self.tokenizer = AutoTokenizer.from_pretrained('allenai/unifiedqa-t5-large', use_fast=False, legacy=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained('allenai/unifiedqa-t5-large')
        self.model.to(self.device)
        self.model.eval()

    def reason_over_evidence(self, question, evidences):
        """
        Combines multiple evidences to answer the question (claim).
        """
        # Combine evidences into a single context
        context = ' '.join(evidences)
        input_text = f"{question} \\n {context}"
        inputs = self.tokenizer.encode(input_text, return_tensors='pt', truncation=True, max_length=1024).to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(inputs, max_length=50)
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer
