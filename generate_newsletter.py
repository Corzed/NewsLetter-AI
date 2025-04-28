import os
from datetime import datetime, timedelta
from OrchestrAI import AgentManager, Agent, AgentTool
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Fetch credentials
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')

# HTML template for the newsletter
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletter</title>
    <style>
        /* General Styles */
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333333;
            background-color: #f9f9f9;
            margin: 0;
            padding: 0;
        }}
        table {{
            border-collapse: collapse;
        }}
        /* Container */
        .container {{
            max-width: 800px;
            width: 100%;
            background-color: #ffffff;
            border-radius: 10px; /* Curved edges */
            overflow: hidden; /* Ensures curved edges are visible */
        }}
        /* Header */
        .header {{
            background-color: #FF9500;
            padding: 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            color: #FFFFFF;
            font-weight: bold;
            border-radius: 10px 10px 0 0; /* Curved top edges */
        }}
        /* Content */
        .content {{
            padding: 20px;
        }}
        .content h2 {{
            color: #333333;
            border-bottom: 2px solid #FF9500;
            padding-bottom: 10px;
            margin-top: 30px;
        }}
        .article {{
            background-color: #FFF8E1;
            border-left: 5px solid #FF9500;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px; /* Curved edges for articles */
        }}
        .article h3 {{
            margin-top: 0;
            color: #333333;
        }}
        .article a {{
            color: #ff7300;
            text-decoration: none;
        }}
        .highlight-box {{
            background-color: #FFE082;
            border-left: 5px solid #FF9500;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px; /* Curved edges for highlight box */
        }}
        /* Mystery Link Button */
        .mystery-link {{
            display: block;
            width: 200px;
            margin: 20px auto;
            padding: 10px 20px;
            background-color: #FF6600;
            color: #ffffff;
            text-align: center;
            text-decoration: none;
            border-radius: 25px; /* Fully curved edges for button */
            font-weight: bold;
        }}
        /* Footer */
        .footer {{
            background-color: #FF9500;
            color: #FFFFFF;
            text-align: center;
            padding: 15px;
            font-size: 12px;
            border-radius: 0 0 10px 10px; /* Curved bottom edges */
        }}
        /* Responsive Adjustments */
        @media only screen and (max-width: 600px) {{
            .container {{
                max-width: 100% !important;
            }}
            .mystery-link {{
                width: 100%;
                padding: 15px 0;
            }}
        }}
    </style>
</head>
<body>
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center" style="padding: 20px 0;">
                <table class="container" cellpadding="0" cellspacing="0" border="0">
                    <!-- Header -->
                    <tr>
                        <td class="header">
                            <h1>Newsletter</h1>
                        </td>
                    </tr>
                    <!-- Content -->
                    <tr>
                        <td class="content" style="padding:20px;">
                            {content}
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td class="footer">
                            <p>© 2025 Newsletter. All rights reserved.</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

def fetch_news(topic: str, days: int = 7) -> str:
    """
    Fetches recent news articles for a given topic using NewsAPI.
    Returns a JSON-formatted string of articles.
    """
    import requests, json
    to_date = datetime.utcnow()
    from_date = to_date - timedelta(days=days)
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': topic,
        'language': 'en',
        'from': from_date.strftime('%Y-%m-%d'),
        'to': to_date.strftime('%Y-%m-%d'),
        'sortBy': 'relevancy',
        'pageSize': 10,
        'apiKey': NEWSAPI_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    articles = response.json().get('articles', [])
    # Simplify articles for agent consumption
    simple = [{'title': a['title'], 'description': a['description'], 'url': a['url']} for a in articles]
    return json.dumps(simple)

# Initialize OrchestrAI
manager = AgentManager()

# Register fetch_news as a tool
news_tool = AgentTool(
    name="fetch_news",
    description="Fetch news articles for a given topic and time range",
    func=fetch_news
)

# Create the agent
NewsAgent = Agent(
    name="NewsAgent",
    role=("You are a newsletter generator. Use the fetch_news tool to gather articles, "
          "then assemble them into an HTML newsletter following the provided template."),
    description="Generates HTML newsletters on AI topics",
    manager=manager,
    tools={"fetch_news": news_tool},
    verbose=True,
    model="gpt-4.1-mini"
)

def generate_newsletter(topic: str) -> str:
    """
    Uses the OrchestrAI agent to generate an HTML newsletter
    for the specified topic.
    """
    # System prompt to guide the agent
    user_prompt = (
        f"""
        Generate a newsletter about {topic} using the following format:

        1. Write a brief, engaging introduction paragraph (2-3 sentences) summarizing the key themes or highlights. Do not make a title.

        2. Create 4-5 sections, each focusing on a specific aspect of {topic}. Make sure the topics are interesting and attention grabbing enough to be put in the news letter. Incorperate Emojis. For each section:
           a. Use an <h2> tag for an intriguing section heading.
           b. Include 2 articles. For each article, use this exact structure:
              <div class="article">
                  <h3><a href="[REAL_ARTICLE_URL]">[Captivating Article Title]</a></h3>
                  <p>[2-3 sentences or/and bullet points summarizing the article with engaging insights or a teaser]</p>
              </div>

        3. After the second section, add a highlight box with an interesting fact or quote:
           <div class="highlight-box">
               <p>[Interesting fact or quote related to the topic]</p>
           </div>

        4. After the 3 sections, generate a "Mystery Link" feature that links to a random mystery url on the topic. (Don't forget to replace the placeholder with a link YOU find!!):
           <a href="placeholder" class="mystery-link" style="color: #ffffff;">Mystery Link!</a>

        5. End with a brief, compelling conclusion paragraph (2-3 sentences) that summarizes the key points.

        6. Use only the HTML tags specified above (<h1>, <h2>, <h3>, <p>, <div>, <a>) and ensure to use the correct classes as shown.

        7. Ensure all content is factual and based on real, current news about {topic}. Use the fetch_news function to get real, recent articles for each section.

        8. The total content should be between 1000-2000 words to keep the newsletter concise and email-friendly.

        9. Throughout the newsletter, use engaging language and interesting facts to keep the reader's attention. Avoid using emojis or any special characters that might not render well in all email clients.

        10. Take the best topic of the newsletter and use the tool to set the email subject to it. (Must be less than 7 words.)

        (Use many different search topics, making sure hey are all no longer than 7 days old)

        Strictly adhere to this format and structure while making the content engaging and suitable for an email newsletter. Make sure not to include code formatting.
        """
    )
    # Run the agent conversation
    html_body = NewsAgent.run_conversation(user_prompt)
    # Combine with our template
    full_html = HTML_TEMPLATE.format(content=html_body)
    return full_html

if __name__ == "__main__":
    topic = os.getenv('NEWS_TOPIC', 'AI')
    newsletter_html = generate_newsletter(topic)
    output_path = os.path.join(os.getcwd(), 'latest_newsletter.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(newsletter_html)
    print(f"Newsletter saved to {output_path}")
