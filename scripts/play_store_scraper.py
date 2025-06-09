# scripts/scrape_reviews.py

from google_play_scraper import Sort, reviews
import pandas as pd
from tqdm import tqdm

apps = {
    "CBE": "com.combanketh.mobilebanking",  
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp"
}

def fetch_reviews(app_id, bank_name, max_reviews=400):
    all_reviews = []
    next_token = None
    print(f"Fetching reviews for {bank_name}...")
    
    while len(all_reviews) < max_reviews:
        batch, next_token = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=200,
            continuation_token=next_token
        )
        all_reviews.extend(batch)
        if not next_token:
            break
    
    df = pd.DataFrame(all_reviews)
    df = df[['content', 'score', 'at']].copy()
    df.columns = ['review', 'rating', 'date']
    df['bank'] = bank_name
    df['source'] = 'Google Play'
    return df

if __name__ == "__main__":
    dfs = []
    for bank, app_id in apps.items():
        df = fetch_reviews(app_id, bank)
        dfs.append(df)
    
    all_reviews = pd.concat(dfs, ignore_index=True)
    all_reviews.to_csv("../data/raw_reviews.csv", index=False)
    print("Saved to data/raw_reviews.csv")
