

# Load the small, lightweight English language model from spaCy
import spacy
from spacy import pipeline
from spacy import pipeline
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    Cleans raw text by lowering case, removing stop words/punctuation, 
    and reducing words to their base dictionary forms.
    """
    if not isinstance(text, str):
        return ""
    
    # Process text through spaCy's NLP pipeline
    doc = nlp(text.lower())
    
    # Tokenize, remove stop words/punctuation/symbols, and lemmatize
    cleaned_tokens = [
        token.lemma_ for token in doc 
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    
    return " ".join(cleaned_tokens)

print("Initializing DistilBERT sentiment pipeline...")
# Initialize the pipeline with the requested model card
sentiment_analyzer = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiment_batch(texts, batch_size=32):
    """
    Runs text batches through the transformer model to calculate 
    labels and confidence scores cleanly.
    """
    results = []
    # Loop over texts in batches to protect system memory
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        # Replace empty strings with a default filler to prevent model crashes
        batch = [t if t.strip() != "" else "neutral product performance" for t in batch]
        
        batch_results = sentiment_analyzer(batch)
        results.extend(batch_results)
    return results


def extract_top_keywords_per_bank(dataframe, text_col, bank_name, top_n=10):
    """
    Extracts the most statistically significant terms for a given bank 
    using Term Frequency-Inverse Document Frequency.
    """
    # Filter the dataset to isolate a single bank's reviews
    bank_df = dataframe[dataframe['bank'] == bank_name]
    
    # Configure vectorizer to look at single words and 2-word phrases (bigrams)
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
    
    tfidf_matrix = vectorizer.fit_transform(bank_df[text_col])
    feature_names = vectorizer.get_feature_names_out()
    
    # Calculate the average TF-IDF score for each term across all reviews for this bank
    mean_tfidf_scores = np.asarray(tfidf_matrix.mean(axis=0)).ravel()
    
    # Sort terms by their structural significance weight
    top_indices = mean_tfidf_scores.argsort()[::-1][:top_n]
    
    top_keywords = [(feature_names[i], mean_tfidf_scores[i]) for i in top_indices]
    return top_keywords




# Step 5a: Map keywords into structural business buckets
def map_text_to_theme(text):
    """
    Categorizes reviews into actionable operational business buckets 
    based on the presence of dominant keyword indicators.
    """
    text_lower = str(text).lower()
    
    # Define rules matching keywords to business-relevant issues
    if any(k in text_lower for k in ['login', 'password', 'otp', 'code', 'activation', 'register', 'unable log']):
        return "Account Access Issues"
    elif any(k in text_lower for k in ['transfer', 'send', 'send money', 'deduct', 'transaction', 'payment', 'failed']):
        return "Transaction Performance"
    elif any(k in text_lower for k in ['crash', 'freeze', 'slow', 'loading', 'bug', 'open', 'network', 'error']):
        return "App Stability & Speed"
    elif any(k in text_lower for k in ['ui', 'interface', 'beautiful', 'update', 'design', 'look', 'worst update']):
        return "UI & Design Feedback"
    elif any(k in text_lower for k in ['feature', 'fingerprint', 'biometric', 'dark mode', 'add', 'request']):
        return "Feature Requests"
    else:
        return "General User Feedback"


