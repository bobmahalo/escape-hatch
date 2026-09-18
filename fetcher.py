import feedparser
import re
from datetime import datetime

# We are using BBC and NPR as our 'Wire Core' proxy since AP/Reuters 
# often deprecate their public RSS feeds or hide them behind paywalls.
# These are highly factual, low-spin sources.
FEEDS = [
    {"name": "BBC World", "url": "http://feeds.bbci.co.uk/news/world/rss.xml"},
    {"name": "NPR World", "url": "https://feeds.npr.org/1004/rss.xml"},
    {"name": "NPR Politics", "url": "https://feeds.npr.org/1014/rss.xml"}
]

def fetch_top_stories():
    """
    Fetches the top stories from our base reality feeds, formats them,
    and returns a single text payload to be sent to the LLM.
    """
    all_stories = []
    
    for feed_info in FEEDS:
        print(f"Fetching from {feed_info['name']}...")
        feed = feedparser.parse(feed_info["url"])
        
        # Grab top 7 from each to ensure enough raw material for the LLM to synthesize
        for entry in feed.entries[:7]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            
            # Strip basic HTML tags from summary
            summary = re.sub('<[^<]+>', '', summary)
            
            if title:
                story = f"Source: {feed_info['name']}\nHeadline: {title}\nSummary: {summary}\n---"
                all_stories.append(story)
                
    return "\n".join(all_stories)

if __name__ == "__main__":
    payload = fetch_top_stories()
    print(f"Fetched {len(payload.split('---')) - 1} raw stories.")
    with open("raw_payload.txt", "w") as f:
        f.write(payload)
    print("Saved to raw_payload.txt for testing.")
