import json
from datetime import datetime

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Escape Hatch</title>
    <style>
        body {{
            font-family: 'Georgia', serif;
            background-color: #f7f7f6;
            color: #2c2c2c;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
        }}
        .container {{
            max-width: 650px;
            width: 100%;
        }}
        header {{
            border-bottom: 2px solid #e0e0df;
            padding-bottom: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        h1 {{
            font-weight: normal;
            font-size: 24px;
            letter-spacing: 1px;
            margin: 0;
            text-transform: uppercase;
        }}
        .date {{
            color: #666;
            font-size: 14px;
            font-style: italic;
        }}
        .story {{
            margin-bottom: 35px;
        }}
        .headline {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        ul {{
            list-style-type: square;
            padding-left: 20px;
            margin-top: 0;
        }}
        li {{
            margin-bottom: 8px;
            font-size: 16px;
        }}
        footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #e0e0df;
            font-style: italic;
            color: #888;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>The Escape Hatch</h1>
            <div class="date">{date}</div>
        </header>
        
        <div id="content">
            {content}
        </div>
        
        <footer>
            You are caught up. Close the app.
        </footer>
    </div>
</body>
</html>
"""

def build_html():
    try:
        with open("filtered_stories.json", "r") as f:
            stories = json.load(f)
    except FileNotFoundError:
        print("Error: filtered_stories.json not found.")
        return
        
    content_html = ""
    for story in stories:
        content_html += f"""
        <div class="story">
            <div class="headline">{story.get('headline', 'Untitled')}</div>
            <ul>
                <li><strong>The Event:</strong> {story.get('event', '')}</li>
                <li><strong>The Context:</strong> {story.get('context', '')}</li>
                <li><strong>The Scope:</strong> {story.get('scope', '')}</li>
            </ul>
        </div>
        """
        
    today = datetime.now().strftime("%B %d, %Y")
    final_html = HTML_TEMPLATE.format(date=today, content=content_html)
    
    with open("index.html", "w") as f:
        f.write(final_html)
        
if __name__ == "__main__":
    build_html()
    print("Built index.html successfully.")
