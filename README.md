# Newsletter Generator

A simple Python-based newsletter generator that uses the OrchestrAI framework and NewsAPI to fetch recent articles on a given topic and assemble them into a styled HTML newsletter.

## Features

- Fetches recent, relevant articles from NewsAPI
- Uses an OrchestrAI agent (`NewsAgent`) to generate an engaging, multi-section newsletter in HTML
- Applies a clean, responsive email template with curved edges, highlight boxes, and a “mystery link” feature
- Outputs a single HTML file (`latest_newsletter.html`) ready to send

## Prerequisites

- **Python** 3.8 or higher
- A **NewsAPI** account and API key (get one at [https://newsapi.org/](https://newsapi.org/))

## Installation

1. Clone this repository

   ```bash
   git clone https://github.com/corzed/newsletter-ai.git
   cd newsletter-generator
   ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following variables:

   ```dotenv
   NEWSAPI_KEY=your_newsapi_key_here
   NEWS_TOPIC=AI              # optional; defaults to "AI"
   ```

## Usage

```bash
python generate_newsletter.py
```

This will:

1. Fetch recent articles on the topic specified by `NEWS_TOPIC` (or `"AI"` by default).
2. Run the OrchestrAI `NewsAgent` to assemble the newsletter body.
3. Wrap it in the HTML template and save it as `latest_newsletter.html`.

## Project Structure

```
.
├── generate_newsletter.py   # Main script
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── example_letter.html      # Example newsletter generated with the tool
```

