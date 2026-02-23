import requests
import json

# Define topics
TOPICS = ["Circular Economy", "Carbon Management", "CSRD/CSDDD Compliance", "Sustainable Materials"]

# Fetch articles from NewsAPI
def fetch_articles(api_key, topics, num_articles=10):
    articles = []
    for topic in topics:
        response = requests.get(f'https://newsapi.org/v2/everything?q={topic}&from=2026-02-16&sortBy=publishedAt&apiKey={api_key}&pageSize={num_articles}')
        if response.status_code == 200:
            data = response.json()
            articles.extend(data['articles'])
    return articles

# Identify trends using GPT-4o-mini (placeholder implementation)
def identify_trends(articles):
    trends = []
    for article in articles:
        # Placeholder for actual GPT-4o-mini interaction
t        summary = f"Key takeaways for {article['title']}"  # Replace with actual GPT-4o-mini integration
        relevance = "High"  # Replace with actual relevance scoring
        trends.append({"title": article['title'], "summary": summary, "relevance": relevance})
    return trends

# Output data in Markdown and JSON formats
def output_results(trends, output_dir):
    # Markdown output
    with open(f'{output_dir}/RAW_DATA.md', 'w') as md_file:
        for trend in trends:
            md_file.write(f"## {trend['title']}\n")
            md_file.write(f"### Summary: {trend['summary']}\n")
            md_file.write(f"### Relevance: {trend['relevance']}\n\n")

    # JSON output
    with open(f'{output_dir}/trends.json', 'w') as json_file:
        json.dump(trends, json_file, indent=4)

# Main function
if __name__ == '__main__':
    API_KEY = 'your_newsapi_key_here'  # Replace with your NewsAPI key
    OUTPUT_DIR = 'path_to_output_directory'  # Set your output directory
    articles = fetch_articles(API_KEY, TOPICS)
    trends = identify_trends(articles)
    output_results(trends, OUTPUT_DIR)