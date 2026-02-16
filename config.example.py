# Example Configuration for the Sustainability Thought Leadership Project

This `config.example.py` file provides an example configuration setup that includes the OpenAI API key and other relevant parameters for content generation.

## Configuration Settings

### OpenAI API Key
To securely store your OpenAI API key, it is recommended to use GitHub Secrets.
1. Go to your GitHub repository.
2. Navigate to 'Settings' > 'Secrets and Variables' > 'Actions'.
3. Click on 'New repository secret'.
4. Name your secret `OPENAI_API_KEY` and paste your OpenAI API key.

You can access the secret in your code using:
```python
import os
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
```

### Trending Topics
Define a list of trending topics to use for content generation:
```python
TRENDING_TOPICS = ['Sustainable Energy', 'Climate Change', 'Circular Economy', 'Biodiversity']
```

### Content Parameters
Customize the content generation parameters:
```python
CONTENT_PARAMETERS = {
    'max_tokens': 150,
    'temperature': 0.7,
    'top_p': 1.0,
    'frequency_penalty': 0,
    'presence_penalty': 0
}
```

Feel free to adjust these settings based on your specific requirements!