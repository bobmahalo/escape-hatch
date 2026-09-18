import os
import sys
import json
from google import genai
from google.genai import types

def get_api_key():
    key_path = os.path.join(os.path.dirname(__file__), 'api_key.txt')
    try:
        with open(key_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def filter_news(raw_payload: str) -> list:
    """
    Takes the raw payload of news stories, sends it to Gemini,
    and returns a structured list of the top 5 distinct stories
    following the 3-bullet structural constraint.
    """
    api_key = get_api_key()
    if not api_key or api_key == "PASTE_YOUR_KEY_HERE":
        print("Error: GEMINI_API_KEY not found in api_key.txt.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are a hyper-clinical, emotionless news editor for a product called "The Escape Hatch".
    Your job is to read the provided raw news payload from various wire services and extract EXACTLY the 5 most globally significant, distinct events of the day.
    
    CRITICAL RULES:
    1. Output EXACTLY 5 stories. No more, no less.
    2. Strip all spin, adjectives, and predictive doom-casting. Use absolute neutral phrasing.
    3. You must format your response as a JSON array of objects.
    
    Each object must have exactly these keys:
    - "headline": A clinical 3-6 word summary of the event.
    - "event": The hard fact of what occurred (1 clear sentence).
    - "context": The historical or political precursor for why this occurred (1 clear sentence).
    - "scope": Who is statistically or directly affected (1 clear sentence).
    
    Raw Payload:
    {raw_payload}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        data = json.loads(response.text)
        return data
    except Exception as e:
        print(f"Failed to generate or parse response: {e}")
        sys.exit(1)

if __name__ == "__main__":
    with open("raw_payload.txt", "r") as f:
        payload = f.read()
    
    print("Filtering news via Gemini...")
    stories = filter_news(payload)
    print(json.dumps(stories, indent=2))
    with open("filtered_stories.json", "w") as f:
        json.dump(stories, f, indent=2)
    print("Saved to filtered_stories.json")
