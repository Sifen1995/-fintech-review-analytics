from google_play_scraper import Sort, reviews
import pandas as pd

# List of apps to scrape
apps = [
    {"name": "CBE", "id": "com.combanketh.mobilebanking"},
    {"name": "BOA", "id": "com.boa.boaMobileBanking"},
    {"name": "Dashen", "id": "com.cr2.amolelight"}
]

all_reviews = []

for app in apps:
    print(f"Scraping {app['name']}...")
    result, continuation_token = reviews(
        app['id'],
        lang='en', # Language of reviews
        country='us', # Target region
        sort=Sort.NEWEST, # Get latest feedback
        count=500 # Slightly more than 400 to ensure enough after cleaning
    )
    
    # Add bank name to each review dictionary
    for res in result:
        res['bank'] = app['name']
        res['source'] = 'Google Play'
    
    all_reviews.extend(result)

# Convert to DataFrame
df = pd.DataFrame(all_reviews)
# Save to CSV
df.to_csv('../data/raw/bank_reviews.csv', index=False)
print("Scraping completed. Reviews saved to bank_reviews.csv")