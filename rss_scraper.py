import feedparser
import csv
import json
import argparse
import sys
from datetime import datetime

def scrape_feeds(config_file, output_csv):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading config file {config_file}: {e}")
        sys.exit(1)

    all_entries = []

    for feed_info in config.get('feeds', []):
        url = feed_info.get('url')
        if not url:
            continue

        name = feed_info.get('name', 'Unknown')
        source = feed_info.get('source', 'Unknown')
        news_type = feed_info.get('news_type', 'Unknown')
        area = feed_info.get('area', 'Unknown')

        print(f"Fetching RSS feed: {url}")
        feed = feedparser.parse(url)

        for entry in feed.entries:
            title = entry.get('title', '')
            link = entry.get('link', '')
            published = entry.get('published', entry.get('updated', ''))

            all_entries.append({
                'name': name,
                'source': source,
                'news_type': news_type,
                'area': area,
                'title': title,
                'link': link,
                'published': published
            })

    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'source', 'news_type', 'area', 'title', 'link', 'published'])
            writer.writeheader()
            writer.writerows(all_entries)
        print(f"Successfully saved {len(all_entries)} feed items to {output_csv}")
    except Exception as e:
        print(f"Error saving to {output_csv}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape RSS feeds and save to CSV.")
    parser.add_argument("--config", default="feeds.json", help="Path to the JSON configuration file")
    parser.add_argument("--output", default="feed_results.csv", help="Path to the output CSV file")
    args = parser.parse_args()

    scrape_feeds(args.config, args.output)
