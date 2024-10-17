# backend/models/ensemble_claim_detection_model.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

class EnsembleClaimDetectionModel:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Load models and tokenizers
        self.models = []
        self.tokenizers = []

        model_names = [
            'Nithiwat/xlm-roberta-base_claim-detection',
            'Nithiwat/mdeberta-v3-base_claim-detection'
        ]

        for model_name in model_names:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(model_name)
            model.to(self.device)
            model.eval()
            self.tokenizers.append(tokenizer)
            self.models.append(model)

        self.label_mapping = {0: 'Non-claim', 1: 'Claim'}

    def predict(self, text):
        logits_list = []
        for tokenizer, model in zip(self.tokenizers, self.models):
            inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512).to(self.device)
            with torch.no_grad():
                outputs = model(**inputs)
            logits = outputs.logits.cpu().numpy()

            # Ensure logits have shape (1, 2)
            if logits.shape[-1] == 2:
                logits_list.append(logits)
            else:
                print(f"Model {model} outputs incompatible logits shape: {logits.shape}")

        if not logits_list:
            raise ValueError("No valid logits collected from models.")

        # Aggregate logits
        logits_array = np.vstack(logits_list)
        avg_logits = np.mean(logits_array, axis=0)
        probabilities = torch.softmax(torch.tensor(avg_logits), dim=-1)
        predicted_class = torch.argmax(probabilities).item()
        confidence = probabilities[predicted_class].item()
        predicted_label = self.label_mapping.get(predicted_class, 'Unknown')

        return predicted_class, predicted_label, confidence
