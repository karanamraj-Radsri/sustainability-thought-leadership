import openai

class ContentGenerator:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_short_post(self, topic):
        prompt = f"Draft a LinkedIn post in first-person C-suite voice about {topic}. The post should be between 400-500 words, focusing on engaging the audience and thought leadership."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']

    def generate_long_post(self, topic):
        prompt = f"Draft a LinkedIn post in first-person C-suite voice about {topic}. The post should be between 500-800 words, focusing on engaging the audience and thought leadership."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']

if __name__ == '__main__':
    # Example usage, replace 'your_api_key' with a valid OpenAI API key
    api_key = 'your_api_key'
    generator = ContentGenerator(api_key)
    trending_topic = "Sustainability in Business"
    print("Short Post:\n", generator.generate_short_post(trending_topic))
    print("Long Post:\n", generator.generate_long_post(trending_topic))