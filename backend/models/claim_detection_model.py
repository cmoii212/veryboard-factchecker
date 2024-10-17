from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class ClaimDetectionModel:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = AutoTokenizer.from_pretrained('Nithiwat/xlm-roberta-base_claim-detection')
        self.model = AutoModelForSequenceClassification.from_pretrained('Nithiwat/xlm-roberta-base_claim-detection')
        self.model.to(self.device)
        self.model.eval()
        self.label_mapping = {0: 'Non-claim', 1: 'Claim'}

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=-1)[0]
        predicted_class = torch.argmax(probabilities).item()
        confidence = probabilities[predicted_class].item()
        predicted_label = self.label_mapping.get(predicted_class, 'Unknown')
        return predicted_class, predicted_label, confidence
