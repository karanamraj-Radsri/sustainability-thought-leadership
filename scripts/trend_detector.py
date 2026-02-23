import requests
import json

# Constants
API_KEY = 'your_newsapi_key'  # Replace with your API key for NewsAPI
TOPICS = ["Climate Change", "Sustainable Agriculture", "Renewable Energy", "Waste Management"]
GPT_MODEL = 'gpt-4o-mini'  # Hypothetical model name, replace with actual model usage

def fetch_articles(topic):
    url = f'https://newsapi.org/v2/everything?q={topic}&pageSize=10&apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        print(f"Error fetching articles for topic {topic}: {response.status_code}")
        return []

def summarize_trends(articles):
    # Mockup function for GPT-4o-mini trend analysis
    # Implement actual call to GPT model here
    return [
        f"Trend {i + 1}: Summary of trend based on {len(articles)} articles."
        for i in range(5)
    ]

def write_output(topic, summaries):
    # Write to JSON file
    with open(f'{topic.replace(" ", "_").lower()}_summary.json', 'w') as json_file:
        json.dump(summaries, json_file)

    # Write to Markdown file
    with open(f'{topic.replace(" ", "_").lower()}_summary.md', 'w') as md_file:
        md_file.write(f"# {topic} Trends\n\n")
        for summary in summaries:
            md_file.write(f"- {summary}\n")

def main():
    for topic in TOPICS:
        articles = fetch_articles(topic)
        if articles:
            summaries = summarize_trends(articles)
            write_output(topic, summaries)

if __name__ == "__main__":
    main()