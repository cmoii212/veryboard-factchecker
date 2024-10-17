import re
import spacy

# Load the spaCy English language model
nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):
    """
    Cleans and preprocesses the input text.
    """
    # Remove URLs, mentions, hashtags
    text = re.sub(r"http\S+|www.\S+|@\S+|#\S+", "", text)
    return text.strip()

def split_into_sentences(text):
    """
    Splits text into sentences using spaCy.
    """
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    return sentences
