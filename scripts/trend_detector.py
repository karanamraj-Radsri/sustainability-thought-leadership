import os
import json
import sys
import datetime
import openai
import requests
from dotenv import load_dotenv

load_dotenv()

class TrendDetector:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')
        self.locked_topics = ["Circular Economy", "Carbon Management", "CSRD/CSDDD Compliance", "Sustainable Materials"]
        self.articles_per_topic = 10
        self.timeframe_days = 7

    def get_week_number(self):
        now = datetime.datetime.utcnow()
        return now.isocalendar()[1]

    def get_date_range(self):
        end_date = datetime.datetime.utcnow()
        start_date = end_date - datetime.timedelta(days=self.timeframe_days)
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    def fetch_articles(self, topic):
        start_date, end_date = self.get_date_range()
        url = f'https://newsapi.org/v2/everything?q={topic}&from={start_date}&to={end_date}&sortBy=publishedAt&pageSize={self.articles_per_topic}&apiKey={self.NEWSAPI_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('articles', [])
        else:
            print(f'Error fetching articles for {topic}: {response.status_code}')
            return []

    def identify_trend_with_gpt(self, article):
        prompt = f'Identify the trend name based on the following article: {article}\n'  
        response = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response.choices[0].message['content']

    def summarize_article_with_gpt(self, article):
        prompt = f'Summarize the following article into 5 bullet points: {article}\n'
        response = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response.choices[0].message['content'].split('\n')

    def assess_relevance(self, article, topic):
        keywords = topic.split()  
        content = article['title'] + ' ' + article['description'] + ' ' + article['content']
        relevance_score = sum(1 for keyword in keywords if keyword.lower() in content.lower())
        if relevance_score >= 2:
            return 'HIGH'
        elif relevance_score == 1:
            return 'MEDIUM'
        else:
            return 'LOW'

    def scan_sources(self):
        all_articles = []
        for topic in self.locked_topics:
            articles = self.fetch_articles(topic)
            for article in articles:
                trend = self.identify_trend_with_gpt(article)
                summary = self.summarize_article_with_gpt(article)
                relevance = self.assess_relevance(article, topic)
                all_articles.append({
                    'article': article,
                    'trend': trend,
                    'summary': summary,
                    'relevance': relevance
                })
        return all_articles

    def save_raw_data_markdown(self, articles):
        week_number = self.get_week_number()
        with open(f'research/# Trending Topics - Week {week_number} - RAW_DATA.md', 'w') as file:
            for article in articles:
                file.write(f"### {article['article']['title']}\n")
                file.write(f"{article['summary']}\n\n")

    def save_raw_data_json(self, articles):
        week_number = self.get_week_number()
        with open(f'research/week-{week_number}-trends-raw.json', 'w') as file:
            json.dump(articles, file, indent=4)

    def run(self):
        articles = self.scan_sources()
        self.save_raw_data_markdown(articles)
        self.save_raw_data_json(articles)

if __name__ == '__main__':
    try:
        if not os.getenv('OPENAI_API_KEY') or not os.getenv('NEWSAPI_KEY'):
            raise ValueError('Missing API keys. Please set OPENAI_API_KEY and NEWSAPI_KEY in .env')
        trend_detector = TrendDetector()
        trend_detector.run()
    except Exception as e:
        print(f'An error occurred: {e}')
