import pytest
import pandas as pd
import os

# Update the path to look inside data/cleaned instead of data/raw
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "cleaned_bank_reviews.csv")

@pytest.fixture
def loaded_data():
    """Fixture to load the data for testing."""
    if not os.path.exists(DATA_PATH):
        pytest.fail(
            f"Cleaned data file not found at {DATA_PATH}. "
            f"Please run your Jupyter notebook (notebooks/task-1.ipynb) to generate the cleaned dataset first."
        )
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
    """Verify that each bank has a healthy amount of reviews after cleaning."""
    counts = loaded_data['bank'].value_counts()
    
    for bank in ['CBE', 'BOA', 'Dashen']:
        assert bank in counts.index, f"Bank '{bank}' not found in the dataset"
        
        # We adjust the threshold to 350 to account for deduplication and textless ratings drops
        assert counts[bank] >= 350, f"{bank} has only {counts[bank]} reviews after filtration, expected 350+"
def test_date_format(loaded_data):
    """Check if dates are properly formatted (YYYY-MM-DD)."""
    date_regex = r'^\d{4}-\d{2}-\d{2}$'
    # Drop any potential NaN strings just in case, then check format
    sample_dates = loaded_data['date'].dropna().astype(str).head(10)
    
    for date in sample_dates:
        assert pd.Series(date).str.match(date_regex).all(), f"Date {date} does not match YYYY-MM-DD"