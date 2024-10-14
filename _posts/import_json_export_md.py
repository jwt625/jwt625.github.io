#%%
import json
import os
from datetime import datetime


#%%
def format_media(media_item, media_folder):
    file_name = os.path.basename(media_item['local_path'])
    new_path = f"/assets/images/2024/{media_folder}/{file_name}"
    return f"![{file_name}]({new_path})"

def create_markdown(json_file, output_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Determine the date range for the media folder name
    all_dates = [datetime.fromisoformat(tweet['timestamp']) for thread in data for tweet in thread['tweets']]
    earliest_date = min(all_dates)
    latest_date = max(all_dates)
    media_folder = f"{earliest_date.strftime('%Y%m%d')}_{latest_date.strftime('%Y%m%d')}"

    with open(output_file, 'w', encoding='utf-8') as f:
        for i, thread in enumerate(data, 1):
            print(i)
            if len(thread['tweets']) == 0:
                continue
            # First tweet in the thread
            first_tweet = thread['tweets'][0]
            f.write(f"{i}. {first_tweet['text']}\n")
            
            # Media for the first tweet
            for media in first_tweet['media']:
                f.write(format_media(media, media_folder) + "\n")
            
            # If there are more tweets in the thread
            if len(thread['tweets']) > 1:
                for tweet in thread['tweets'][1:]:
                    f.write(f"   - {tweet['text']}\n")
                    # Media for this tweet
                    for media in tweet['media']:
                        f.write("   " + format_media(media, media_folder) + "\n")
            
            f.write("\n")  # Add a blank line between threads


#%%
json_file = "scraped_tweets_20240930_20241009.json"
output_file = "blog_post_20240930_20241009.md"
# json_file = "scraped_tmp.json"
# output_file = "blog_post_tmp.md"
create_markdown(json_file, output_file)
print(f"Markdown file '{output_file}' has been created.")
# %%
