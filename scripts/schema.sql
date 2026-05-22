-- Drop tables if they exist so we can run this script repeatedly without errors
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS banks;

-- 1. Create the Banks Lookup Table
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL UNIQUE,
    app_name VARCHAR(150) NOT NULL
);

-- 2. Create the Processed Reviews Table
CREATE TABLE reviews (
    review_id INT PRIMARY KEY,
    bank_id INT NOT NULL,
    review_text TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_date DATE NOT NULL,
    sentiment_label VARCHAR(20) NOT NULL,
    sentiment_score NUMERIC(5, 4) NOT NULL,
    identified_theme VARCHAR(100) NOT NULL,
    source VARCHAR(50) DEFAULT 'Google Play',
    CONSTRAINT fk_bank FOREIGN KEY (bank_id) REFERENCES banks (bank_id) ON DELETE CASCADE
);