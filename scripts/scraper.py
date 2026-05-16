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
        count=900 # Slightly more than 400 to ensure enough after cleaning
    )
    
    # Add bank name to each review dictionary
    for res in result:
        res['bank'] = app['name']
        res['source'] = 'Google Play'
    
    all_reviews.extend(result)

# Convert to DataFrame
df = pd.DataFrame(all_reviews)
# Save to CSV


import os

# 1. Get the path to the root folder of your project dynamically
script_dir = os.path.dirname(os.path.abspath(__file__)) # points to 'scripts'
root_dir = os.path.dirname(script_dir)                  # points to project root

# 2. Build absolute paths to 'data/raw'
target_dir = os.path.join(root_dir, 'data', 'raw')
output_file = os.path.join(target_dir, 'bank_reviews.csv')

# 3. Dynamically create data/raw if it doesn't exist (e.g., on the GitHub runner)
os.makedirs(target_dir, exist_ok=True)

# 4. Save the file
df.to_csv(output_file, index=False)
print(f"Scraping completed. Reviews saved to {output_file}")

