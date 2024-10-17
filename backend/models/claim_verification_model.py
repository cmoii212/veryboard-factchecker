from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class ClaimVerificationModel:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = AutoTokenizer.from_pretrained('MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli')
        self.model = AutoModelForSequenceClassification.from_pretrained('MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli')
        self.model.to(self.device)
        self.model.eval()
        self.label_names = ["entailment", "neutral", "contradiction"]

    def verify(self, claim, evidence):
        inputs = self.tokenizer(claim, evidence, return_tensors='pt', truncation=True).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=-1)[0]
        predicted_class = torch.argmax(probabilities).item()
        confidence = probabilities[predicted_class].item()
        predicted_label = self.label_names[predicted_class]
        return predicted_label, confidence
