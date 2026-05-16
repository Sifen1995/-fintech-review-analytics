import pytest
import pandas as pd
import os

# Path to your cleaned data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "bank_reviews.csv")

@pytest.fixture
def loaded_data():
    """Fixture to load the data for testing."""
    if not os.path.exists(DATA_PATH):
        pytest.fail(f"Cleaned data file not found at {DATA_PATH}. Run the scraping script first.")
    return pd.read_csv(DATA_PATH)
def test_required_columns_exist(loaded_data):
    """Check if all required columns are present in the final dataset."""
    expected_columns = ['review', 'rating', 'date', 'bank', 'source']
    actual_columns = list(loaded_data.columns)
    
    for col in expected_columns:
        assert col in actual_columns, f"Missing required column: {col}"

def test_no_empty_reviews(loaded_data):
    """Ensure there are no null values in the review or rating columns."""
    assert loaded_data['review'].isnull().sum() == 0, "Found null values in 'review' column"
    assert loaded_data['rating'].isnull().sum() == 0, "Found null values in 'rating' column"

def test_minimum_review_count(loaded_data):
    """Verify that each bank has at least 400 reviews as per challenge requirements."""
    counts = loaded_data['bank'].value_counts()
    
    for bank in ['CBE', 'BOA', 'Dashen']:
        # We use a slight buffer (e.g., 380) in case cleaning removed a few, 
        # but 400 is the target goal.
        assert counts[bank] >= 400, f"{bank} has only {counts[bank]} reviews, expected 400+"

def test_date_format(loaded_data):
    """Check if dates are properly formatted (YYYY-MM-DD)."""
    # This regex checks for 4 digits - 2 digits - 2 digits
    date_regex = r'^\d{4}-\d{2}-\d{2}$'
    sample_dates = loaded_data['date'].astype(str).head(10)
    
    for date in sample_dates:
        assert pd.Series(date).str.match(date_regex).all(), f"Date {date} does not match YYYY-MM-DD"