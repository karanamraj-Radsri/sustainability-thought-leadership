import json
import openai

class TrendCurator:
    def __init__(self, json_file):
        self.json_file = json_file
        self.trends = self.load_trends()

    def load_trends(self):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
        return data['trends']

    def score_trends(self):
        scores = {}
        for trend in self.trends:
            score = self.evaluate_trend(trend)
            scores[trend['name']] = score
        return scores

    def evaluate_trend(self, trend):
        # Placeholder for scoring logic using GPT-4o-mini
        relevance = 0  # 0 to 40
        timeliness = 0  # 0 to 30
        novelty = 0  # 0 to 20
        actionability = 0  # 0 to 10
        # Assume some scoring system here
        total_score = relevance * 0.4 + timeliness * 0.3 + novelty * 0.2 + actionability * 0.1
        return total_score

    def generate_markdown(self, scores):
        sorted_trends = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        top_trends = sorted_trends[:3]
        markdown_content = "# Curated Trends\n"
        markdown_content += "## Top 3 Trends:\n"
        for trend in top_trends:
            markdown_content += f'- {trend[0]}: {trend[1]}\n'
        markdown_content += "## All Trends:\n"
        for trend in sorted_trends:
            markdown_content += f'- {trend[0]}: {trend[1]}\n'
        return markdown_content

    def save_markdown(self, markdown_content):
        with open('curated_trends.md', 'w') as file:
            file.write(markdown_content)

    def create_issue(self, markdown_content):
        issue_title = 'Trend Review'
        issue_body = f"## Curated Trends\n{markdown_content}"
        # Placeholder for GitHub API call to create an issue
        print("Issue created with title: " + issue_title)

    def run(self):
        scores = self.score_trends()
        markdown_content = self.generate_markdown(scores)
        self.save_markdown(markdown_content)
        self.create_issue(markdown_content)
