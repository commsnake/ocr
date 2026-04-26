import feedparser
import csv
import json
import argparse
import sys
from datetime import datetime
from duckduckgo_search import DDGS
import time

def get_alternate_sources(query, num_results=3):
    results = []
    try:
        ddgs_gen = DDGS().text(query, max_results=num_results)
        for r in ddgs_gen:
            results.append({
                'title': r.get('title', ''),
                'href': r.get('href', ''),
                'body': r.get('body', '')
            })
    except Exception as e:
        print(f"Error fetching alternate sources for '{query}': {e}")
    return results

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

        # To avoid being rate limited and taking too long, we will limit entries per feed
        # for this demonstration.
        max_entries_per_feed = 3
        count = 0

        for entry in feed.entries:
            if count >= max_entries_per_feed:
                break

            title = entry.get('title', '')
            link = entry.get('link', '')
            published = entry.get('published', entry.get('updated', ''))

            print(f"  Processing story: {title[:50]}...")
            # Use the title to find alternate sources/opinions
            # We strip common quotes to improve search
            clean_title = title.replace('"', '').replace("'", "")
            alt_sources = get_alternate_sources(clean_title, num_results=3)

            # Format alternate sources into a readable string
            alt_sources_text = ""
            for i, src in enumerate(alt_sources):
                alt_sources_text += f"[{i+1}] {src['title']} - {src['href']} ({src['body'][:100]}...)\n"

            all_entries.append({
                'name': name,
                'source': source,
                'news_type': news_type,
                'area': area,
                'title': title,
                'link': link,
                'published': published,
                'alternate_sources': alt_sources_text.strip()
            })

            count += 1
            time.sleep(1) # Be polite to the search API

    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['name', 'source', 'news_type', 'area', 'title', 'link', 'published', 'alternate_sources']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_entries)
        print(f"Successfully saved {len(all_entries)} feed items with alternate sources to {output_csv}")
    except Exception as e:
        print(f"Error saving to {output_csv}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape RSS feeds, find alternate opinions via DuckDuckGo, and save to CSV.")
    parser.add_argument("--config", default="feeds.json", help="Path to the JSON configuration file")
    parser.add_argument("--output", default="feed_results.csv", help="Path to the output CSV file")
    args = parser.parse_args()

    scrape_feeds(args.config, args.output)
