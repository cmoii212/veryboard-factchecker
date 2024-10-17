# backend/evaluate_app.py

import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
import time
import os
import sys

# Adjust the Python path to include the backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_dir)

# Import your application's models and utilities
from models.ensemble_claim_detection_model import EnsembleClaimDetectionModel
from models.advanced_claim_verification_model import AdvancedClaimVerificationModel
from models.multi_hop_reasoning_model import MultiHopReasoningModel
from models.question_answering_model import QuestionAnsweringModel
from utils.text_preprocessing import preprocess_text
from utils.evidence_retrieval import retrieve_evidence
from utils.relevance_filtering import RelevanceFilter
from utils.similarity import SimilarityCalculator
from utils.knowledge_graph import query_wikidata, extract_texts_from_kg_results

# Initialize models
claim_detector = EnsembleClaimDetectionModel()
claim_verifier = AdvancedClaimVerificationModel()
similarity_calculator = SimilarityCalculator()
relevance_filter = RelevanceFilter(model=similarity_calculator.model)
multi_hop_reasoner = MultiHopReasoningModel()
qa_model = QuestionAnsweringModel()

def process_claim(claim_text):
    # Preprocess the claim
    cleaned_claim = preprocess_text(claim_text)

    # Step 1: Claim Detection
    predicted_class, predicted_label, confidence = claim_detector.predict(cleaned_claim)
    if predicted_class != 1:
        # Not a factual claim
        return None, None

    # Step 2: Evidence Retrieval
    evidence_list = retrieve_evidence(cleaned_claim)
    if not evidence_list:
        return 'Not Enough Information', 0.0

    relevant_evidences = []
    evidence_sources = []

    # Process evidence from web search
    for evidence in evidence_list:
        full_content = evidence['content']
        if not full_content:
            continue

        # Extract relevant passages
        relevant_text = relevance_filter.extract_relevant_passages(cleaned_claim, full_content, top_k=3)
        if not relevant_text:
            continue

        # Compute similarity
        similarity_score = similarity_calculator.compute_similarity(cleaned_claim, relevant_text)

        threshold = 0.5  # Adjust as needed
        if similarity_score >= threshold:
            relevant_evidences.append(relevant_text)
            evidence_sources.append(evidence['url'])
        else:
            continue

    # Knowledge Graph Query
    kg_results = query_wikidata(cleaned_claim)
    kg_evidences = extract_texts_from_kg_results(kg_results)
    if kg_evidences:
        relevant_evidences.extend(kg_evidences)
        for result in kg_results.get("results", {}).get("bindings", []):
            item_url = result["item"]["value"]
            evidence_sources.append(item_url)
    time.sleep(1)  # To prevent rate limiting

    if not relevant_evidences:
        return 'Not Enough Information', 0.0

    verifications = []

    # Use QA Model for Fact Extraction
    for idx, evidence_text in enumerate(relevant_evidences):
        answer, score = qa_model.extract_answer(cleaned_claim, evidence_text)
        if score > 0.1:
            # Verify the claim
            predicted_label, confidence = claim_verifier.verify(cleaned_claim, answer)
            verifications.append({
                'label': predicted_label,
                'confidence': confidence
            })
        else:
            continue

    # Multi-Hop Reasoning
    if len(relevant_evidences) > 1:
        answer = multi_hop_reasoner.reason_over_evidence(cleaned_claim, relevant_evidences)
        predicted_label, confidence = claim_verifier.verify(cleaned_claim, answer)
        verifications.append({
            'label': predicted_label,
            'confidence': confidence
        })

    if not verifications:
        return 'Not Enough Information', 0.0

    # Aggregation of Results
    labels = [v['label'] for v in verifications]
    final_label = max(set(labels), key=labels.count)
    average_confidence = sum([v['confidence'] for v in verifications]) / len(verifications)

    return final_label, average_confidence

def map_ground_truth_label(label):
    # Map LIAR dataset labels to your application's labels
    label_mapping = {
        'true': 'Supported',
        'mostly-true': 'Supported',
        'half-true': 'Not Enough Information',
        'barely-true': 'Refuted',
        'false': 'Refuted',
        'pants-fire': 'Refuted'
    }
    return label_mapping.get(label.lower(), 'Not Enough Information')

def main():
    # Adjust the path to the dataset
    dataset_path = os.path.join(backend_dir, 'data', 'train.tsv')
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return

    # Load the LIAR dataset
    liar_df = pd.read_csv(dataset_path, sep='\t', header=None)
    liar_df.columns = [
        'id', 'label', 'statement', 'subject', 'speaker', 'speaker_job_title',
        'state_info', 'party_affiliation', 'barely_true_counts', 'false_counts',
        'half_true_counts', 'mostly_true_counts', 'pants_on_fire_counts',
        'context'
    ]

    # Lists to store results
    y_true = []
    y_pred = []

    total_samples = len(liar_df)
    print(f"Total samples to process: {total_samples}")

    for index, row in liar_df.iterrows():
        claim_text = row['statement']
        ground_truth_label = map_ground_truth_label(row['label'])
        print(f"\nProcessing claim {index + 1}/{total_samples}: {claim_text}")
        print(f"Ground truth label: {ground_truth_label}")

        predicted_label, confidence = process_claim(claim_text)
        if predicted_label is None:
            # Claim was not detected as a factual claim
            predicted_label = 'Not a Claim'

        print(f"Predicted label: {predicted_label}, Confidence: {confidence}")

        y_true.append(ground_truth_label)
        y_pred.append(predicted_label)

    # Evaluation Metrics
    labels = ['Supported', 'Refuted', 'Not Enough Information', 'Not a Claim']
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, labels=labels, digits=4))

    # Overall Accuracy
    accuracy = accuracy_score(y_true, y_pred)
    print(f"Overall Accuracy: {accuracy:.4f}")

if __name__ == "__main__":
    main()
