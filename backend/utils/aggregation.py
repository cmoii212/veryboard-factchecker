def aggregate_results(verifications):
    """
    Aggregates the verification results from multiple pieces of evidence.
    """
    counts = {'True': 0, 'Uncertain': 0, 'False': 0}
    total_confidence = {'True': 0.0, 'Uncertain': 0.0, 'False': 0.0}

    label_mapping = {
        'entailment': 'True',
        'neutral': 'Uncertain',
        'contradiction': 'False'
    }

    for v in verifications:
        predicted_label = label_mapping[v['label']]
        counts[predicted_label] += 1
        total_confidence[predicted_label] += v['confidence']

    final_class = max(counts, key=counts.get)
    average_confidence = total_confidence[final_class] / counts[final_class] if counts[final_class] > 0 else 0

    return final_class, average_confidence
