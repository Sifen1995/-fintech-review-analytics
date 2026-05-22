import os
import pandas as pd
from sqlalchemy import create_engine, text

# Database Connection Parameters for Docker
DB_USER = "fintech_user"
DB_PASSWORD = "fintech_password"
DB_HOST = "localhost"
DB_PORT = "15432"
DB_NAME = "fintech_db"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# Dynamic path tracking
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if '__file__' in locals() else os.getcwd()
SCHEMA_PATH = os.path.join(BASE_DIR, "scripts", "schema.sql")
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "processed_sentiment_reviews.csv")

def initialize_database():
    """Reads schema.sql and builds the structure inside the Docker PostgreSQL instance."""
    print("Reading schema.sql and creating tables...")
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()
    
    with engine.begin() as conn:
        conn.execute(text(schema_sql))
    print("✅ Database tables initialized successfully.")

def populate_banks_metadata():
    """Seeds the static banks lookup table and returns a name-to-id mapping dictionary."""
    print("Seeding 'banks' lookup metadata...")
    banks_data = [
        {"bank_name": "CBE", "app_name": "Commercial Bank of Ethiopia"},
        {"bank_name": "BOA", "app_name": "Bank of Abyssinia"},
        {"bank_name": "Dashen", "app_name": "Dashen Bank"}
    ]
    
    with engine.begin() as conn:
        # Clear existing banks to avoid conflicts
        conn.execute(text("TRUNCATE TABLE banks CASCADE;"))
        
        for bank in banks_data:
            query = text("""
                INSERT INTO banks (bank_name, app_name) 
                VALUES (:bank_name, :app_name)
            """)
            conn.execute(query, bank)
            
    # Retrieve the auto-generated serial IDs from the database
    with engine.connect() as conn:
        result = conn.execute(text("SELECT bank_name, bank_id FROM banks;"))
        return {row[0]: row[1] for row in result}

def upload_reviews_to_postgres(bank_id_map):
    """Loads the processed NLP dataset, maps bank strings to IDs, and uploads to PostgreSQL."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Missing Task 2 dataset at: {DATA_PATH}. Run Task 2 first!")
        
    print("Loading NLP processed dataset...")
    processed_df = pd.read_csv(DATA_PATH)
    
    # Load the original cleaned data to get bank, date, rating, and source columns
    cleaned_data_path = os.path.join(BASE_DIR, "data", "raw", "cleaned_bank_reviews.csv")
    cleaned_df = pd.read_csv(cleaned_data_path)
    
    # Rename 'review' column in cleaned data to 'review_text' for consistent merging
    cleaned_df = cleaned_df.rename(columns={'review': 'review_text'})
    
    # Merge processed NLP results with original cleaned data on review_text
    df = pd.merge(cleaned_df, processed_df, on='review_text', how='left')
    
    # Drop duplicates based on review_text to avoid duplicate key errors
    df = df.drop_duplicates(subset=['review_text'], keep='first')
    
    # Reset review_id to ensure uniqueness
    df = df.reset_index(drop=True)
    df['review_id'] = range(1, len(df) + 1)
    
    # Ensure date column is formatted correctly for SQL DATE types
    df['review_date'] = pd.to_datetime(df['date']).dt.date
    
    # Map the text bank identifier (e.g., 'CBE') to its relational integer bank_id
    df['bank_id'] = df['bank'].map(bank_id_map)
    
    # Select and rename columns to match the SQL schema exactly
    final_df = df[[
        'review_id', 'bank_id', 'review_text', 'rating', 
        'review_date', 'sentiment_label', 'sentiment_score', 'identified_theme', 'source'
    ]]
    
    print(f"Streaming {len(final_df)} records directly into your Docker PostgreSQL database...")
    
    # Use direct SQL INSERT instead of pandas to_sql to avoid compatibility issues
    with engine.begin() as conn:
        # Clear existing data to avoid duplicate key errors
        conn.execute(text("TRUNCATE TABLE reviews;"))
        
        for idx, row in final_df.iterrows():
            insert_query = text("""
                INSERT INTO reviews 
                (review_id, bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, identified_theme, source)
                VALUES (:review_id, :bank_id, :review_text, :rating, :review_date, :sentiment_label, :sentiment_score, :identified_theme, :source)
            """)
            conn.execute(insert_query, {
                'review_id': row['review_id'],
                'bank_id': int(row['bank_id']) if pd.notna(row['bank_id']) else None,
                'review_text': row['review_text'],
                'rating': int(row['rating']) if pd.notna(row['rating']) else None,
                'review_date': row['review_date'],
                'sentiment_label': row['sentiment_label'],
                'sentiment_score': float(row['sentiment_score']) if pd.notna(row['sentiment_score']) else None,
                'identified_theme': row['identified_theme'],
                'source': row['source']
            })
    
    print("🎉 Data injection successfully completed!")

if __name__ == "__main__":
    # Run the full automation pipeline
    initialize_database()
    bank_map = populate_banks_metadata()
    upload_reviews_to_postgres(bank_map)