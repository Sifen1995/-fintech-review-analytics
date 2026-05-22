from sqlalchemy import create_engine, text

# Database Connection Parameters for Docker
DB_USER = "fintech_user"
DB_PASSWORD = "fintech_password"
DB_HOST = "localhost"
DB_PORT = "15432"
DB_NAME = "fintech_db"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

queries = {
    "1. Review Volume Per Bank": """
        SELECT b.bank_name, COUNT(r.review_id) as total_stored_reviews 
        FROM reviews r
        JOIN banks b ON r.bank_id = b.bank_id
        GROUP BY b.bank_name;
    """,
    "2. Core Performance KPI Profiles": """
        SELECT b.bank_name, ROUND(AVG(r.rating), 2) as average_star_rating, COUNT(CASE WHEN r.sentiment_label = 'NEGATIVE' THEN 1 END) as negative_review_count
        FROM reviews r
        JOIN banks b ON r.bank_id = b.bank_id
        GROUP BY b.bank_name;
    """,
    "3. Missing/Null Field Audit": """
        SELECT COUNT(*) as dirty_rows_found 
        FROM reviews 
        WHERE review_text IS NULL OR rating IS NULL OR bank_id IS NULL;
    """
}

print("Running Automated Data Quality Controls...")
with engine.connect() as conn:
    for title, sql in queries.items():
        print(f"\n--- {title} ---")
        result = conn.execute(text(sql))
        for row in result:
            print(dict(row._mapping))