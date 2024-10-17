from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class AdvancedClaimVerificationModel:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # Use a suitable pre-trained model
        self.tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-mnli')
        self.model = AutoModelForSequenceClassification.from_pretrained('facebook/bart-large-mnli')
        self.model.to(self.device)
        self.model.eval()
        self.nli_labels = ["contradiction", "neutral", "entailment"]
        # Map NLI labels to application labels
        self.label_mapping = {
            "entailment": "Supported",
            "contradiction": "Refuted",
            "neutral": "Not Enough Information"
        }

    def verify(self, claim, evidence):
        inputs = self.tokenizer(claim, evidence, return_tensors='pt', truncation=True, max_length=512).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=-1)[0]
        predicted_class = torch.argmax(probabilities).item()
        confidence = probabilities[predicted_class].item()
        nli_label = self.nli_labels[predicted_class]
        predicted_label = self.label_mapping[nli_label]
        return predicted_label, confidence
