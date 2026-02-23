import os
import json
import glob
from datetime import datetime
from typing import List, Dict

class TrendCurator:
    def __init__(self, json_data: Dict):
        self.data = json_data
        self.trends = self.extract_trends()

    def extract_trends(self) -> List[Dict]:
        # Logic to extract trends from JSON data
        trends = []
        for trend in self.data.get('trends', []):
            trends.append(trend)
        return trends

    def score_trend(self, trend: Dict) -> float:
        # Scoring logic based on relevance, timeliness, novelty, actionability
        relevance = trend.get('relevance', 0) * 0.4
        timeliness = trend.get('timeliness', 0) * 0.3
        novelty = trend.get('novelty', 0) * 0.2
        actionability = trend.get('actionability', 0) * 0.1
        return relevance + timeliness + novelty + actionability

    def rank_trends(self):
        for trend in self.trends:
            trend['score'] = self.score_trend(trend)
        self.trends.sort(key=lambda x: x['score'], reverse=True)

    def generate_markdown(self) -> str:
        # Generate the markdown output
        output = "# Ranked Trends\n\n"
        for i, trend in enumerate(self.trends[:3]):
            output += f"## Trend {i + 1}: {trend['name']}\n"
            output += f"Score: {trend['score']}\n\n"
        output += "### Other Trends\n\n"
        for trend in self.trends[3:]:
            output += f"- {trend['name']}\n"
        return output

def main():
    # Find the latest JSON file in the research directory
    list_of_files = glob.glob('research/*.json')
    latest_file = max(list_of_files, key=os.path.getctime)

    # Load the JSON data
    with open(latest_file, 'r') as file:
        json_data = json.load(file)
    
    # Run the curator
    curator = TrendCurator(json_data)
    curator.rank_trends()
    markdown_output = curator.generate_markdown()

    # Save markdown output
    with open('output/trends.md', 'w') as md_file:
        md_file.write(markdown_output)

if __name__ == '__main__':
    main()