# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.text_retrieval import retrieve_post_text
from utils.text_preprocessing import preprocess_text, split_into_sentences
from models.ensemble_claim_detection_model import EnsembleClaimDetectionModel
from models.advanced_claim_verification_model import AdvancedClaimVerificationModel
from models.multi_hop_reasoning_model import MultiHopReasoningModel
from models.question_answering_model import QuestionAnsweringModel
from utils.evidence_retrieval import retrieve_evidence
from utils.relevance_filtering import RelevanceFilter
from utils.similarity import SimilarityCalculator
from utils.knowledge_graph import query_wikidata, extract_texts_from_kg_results
import time

app = Flask(__name__)
CORS(app)

# Initialize models
claim_detector = EnsembleClaimDetectionModel()
claim_verifier = AdvancedClaimVerificationModel()
similarity_calculator = SimilarityCalculator()
relevance_filter = RelevanceFilter(model=similarity_calculator.model)
multi_hop_reasoner = MultiHopReasoningModel()
qa_model = QuestionAnsweringModel()

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url')
    text = data.get('text')

    if not url and not text:
        return jsonify({'error': 'No URL or text provided.'}), 400

    # Step 1: Text Retrieval
    if url:
        print(f"Received request to analyze URL: {url}")
        text = retrieve_post_text(url)
        if not text:
            print("Unable to retrieve text from the provided URL.")
            return jsonify({'error': 'Unable to retrieve text from the provided URL.'}), 400
    else:
        print(f"Received text for analysis.")

    print(f"Text to be analyzed: {text}")

    # Step 2: Text Preprocessing
    cleaned_text = preprocess_text(text)
    sentences = split_into_sentences(cleaned_text)
    print(f"Preprocessed Text: {cleaned_text}")
    print(f"Split into Sentences: {sentences}")

    # Step 3: Claim Detection
    claims = []
    for sentence in sentences:
        predicted_class, predicted_label, confidence = claim_detector.predict(sentence)
        print(f"Analyzing Sentence: {sentence}")
        print(f"Predicted Class: {predicted_class}, Label: {predicted_label}, Confidence: {confidence}")
        if predicted_class == 1:
            claims.append({'sentence': sentence, 'confidence': confidence, 'label': predicted_label})

    if not claims:
        print("No factual claims detected in the text.")
        return jsonify({'message': 'No factual claims detected in the text.'}), 200

    print(f"Detected Claims: {claims}")

    # Step 4 and 5: Evidence Retrieval and Relevance Filtering
    verifications = []
    for claim in claims:
        print(f"Retrieving evidence for claim: {claim['sentence']}")
        evidence_list = retrieve_evidence(claim['sentence'])
        print(f"Evidence List: {evidence_list}")
        if not evidence_list:
            print(f"No evidence found for claim: {claim['sentence']}")
            continue  # Skip if no evidence found

        relevant_evidences = []
        evidence_sources = []  # Collect evidence sources (URLs or 'Wikidata')

        # Process evidence from web search
        for evidence in evidence_list:
            full_content = evidence['content']
            if not full_content:
                continue  # Skip if no content was fetched

            # Extract relevant passages
            relevant_text = relevance_filter.extract_relevant_passages(claim['sentence'], full_content, top_k=9)
            if not relevant_text:
                continue  # Skip if no relevant passages found

            # Compute similarity between claim and extracted passages
            similarity_score = similarity_calculator.compute_similarity(claim['sentence'], relevant_text)

            threshold = 0.3  # Adjust as needed
            if similarity_score >= threshold:
                relevant_evidences.append(relevant_text)
                evidence_sources.append(evidence['url'])  # Use 'url' instead of 'link'
            else:
                print(f"Evidence not relevant enough (similarity: {similarity_score})")

        # Knowledge Graph Query
        print(f"Querying knowledge graph for claim: {claim['sentence']}")
        kg_results = query_wikidata(claim['sentence'])
        kg_evidences = extract_texts_from_kg_results(kg_results)
        if kg_evidences:
            relevant_evidences.extend(kg_evidences)
            # Since KG results don't have URLs, we can use 'Wikidata' or specific item URLs
            for result in kg_results.get("results", {}).get("bindings", []):
                item_url = result["item"]["value"]  # This is the URL to the Wikidata item
                evidence_sources.append(item_url)
        # Add a delay to prevent rate limiting
        time.sleep(1)

        if not relevant_evidences:
            print(f"No relevant evidences found for claim: {claim['sentence']}")
            continue

        # Use QA Model for Fact Extraction
        for idx, evidence_text in enumerate(relevant_evidences):
            answer, score = qa_model.extract_answer(claim['sentence'], evidence_text)
            if score > 0.01:  # Threshold for accepting the answer
                # Verify the claim against the extracted answer
                predicted_label, confidence = claim_verifier.verify(claim['sentence'], answer)
                print(f"Verification Result - Label: {predicted_label}, Confidence: {confidence}")
                verifications.append({
                    'claim': claim['sentence'],
                    'evidence': evidence_text,
                    'evidence_source': evidence_sources[idx],  # Include the source URL
                    'label': predicted_label,
                    'confidence': confidence
                })
            else:
                print(f"No relevant answer found in evidence with score {score}")

        # Use Multi-Hop Reasoning for complex claims
        if len(relevant_evidences) > 1:
            answer = multi_hop_reasoner.reason_over_evidence(claim['sentence'], relevant_evidences)
            predicted_label, confidence = claim_verifier.verify(claim['sentence'], answer)
            print(f"Multi-Hop Verification Result - Label: {predicted_label}, Confidence: {confidence}")
            # Include all evidence sources used in multi-hop reasoning
            verifications.append({
                'claim': claim['sentence'],
                'evidence': answer,
                'evidence_source': evidence_sources,  # Include the list of all sources used
                'label': predicted_label,
                'confidence': confidence
            })

    if not verifications:
        print("No evidence found for the claims.")
        return jsonify({'message': 'No evidence found for the claims.'}), 200

    # Step 6: Aggregation of Results
    final_results = []
    for claim in claims:
        claim_verifications = [v for v in verifications if v['claim'] == claim['sentence']]
        if claim_verifications:
            # Simple majority voting
            labels = [v['label'] for v in claim_verifications]
            final_label = max(set(labels), key=labels.count)
            average_confidence = sum([v['confidence'] for v in claim_verifications]) / len(claim_verifications)
            # Collect evidence links for this claim
            # Flatten the evidence sources if they are lists (from multi-hop reasoning)
            claim_evidence_links = []
            for v in claim_verifications:
                if isinstance(v['evidence_source'], list):
                    claim_evidence_links.extend(v['evidence_source'])
                else:
                    claim_evidence_links.append(v['evidence_source'])
            # Remove duplicates
            claim_evidence_links = list(set(claim_evidence_links))
            final_results.append({
                'claim': claim['sentence'],
                'classification': final_label,
                'confidence': average_confidence,
                'evidence_links': claim_evidence_links  # Include evidence links here
            })

    if not final_results:
        print("No verifiable claims found.")
        return jsonify({'message': 'No verifiable claims found.'}), 200

    return jsonify({'results': final_results}), 200

if __name__ == '__main__':
    app.run(debug=True)
