from semantic_text_similarity.models import WebBertSimilarity
from semantic_text_similarity.models import ClinicalBertSimilarity

def similarity_module(submission, metric):
    model = ClinicalBertSimilarity(device='cpu', batch_size=10) #defaults to GPU prediction
    similarity = {}
    prediction = model.predict([(submission, metric)])
    print(predictions)
    return predictions


