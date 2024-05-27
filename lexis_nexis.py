import requests
import datetime
from requests.auth import HTTPBasicAuth

# Function to read API key and secret from file
def read_api_credentials(file_path):
    with open(file_path, 'r') as file:
        api_key = file.readline().strip()
        api_secret = file.readline().strip()
    return api_key, api_secret

# Define the base URL for the LexisNexis API
BASE_URL = 'https://services-api.lexisnexis.com/v1/News'  # Correct endpoint

# Function to get the past week's top news articles
def get_top_news_articles(api_key, api_secret):
    # Calculate the dates for the past week
    today = datetime.date.today()
    one_week_ago = today - datetime.timedelta(days=7)

    # Prepare headers
    headers = {
        'Content-Type': 'application/json'
    }

    # Define the query parameters
    params = {
        'startDate': one_week_ago.isoformat(),
        'endDate': today.isoformat(),
        'sort': 'relevance'  # or 'date' for latest articles
    }

    # Make the API request with Basic Authentication
    response = requests.get(BASE_URL, 
                            headers=headers, 
                            params=params, 
                            auth=HTTPBasicAuth(api_key, api_secret))

    # Check if the request was successful
    if response.status_code == 200:
        try:
            articles = response.json().get('articles', [])
            return articles
        except requests.exceptions.JSONDecodeError:
            print("Error decoding the JSON response.")
            return []
    else:
        print(f"Failed to fetch articles: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    # Path to the file containing API credentials
    credentials_file = 'lexis_nexis_key.txt'

    # Read the API credentials
    API_KEY, API_SECRET = read_api_credentials(credentials_file)

    # Fetch the top news articles
    articles = get_top_news_articles(API_KEY, API_SECRET)

    # Print the fetched articles
    for idx, article in enumerate(articles):
        print(f"{idx + 1}. {article['title']}")
        print(f"Published on: {article['publicationDate']}")
        print(f"Source: {article['source']['name']}")
        print(f"URL: {article['url']}")
        print("Summary:", article.get('summary', 'No summary available'))
        print("-" * 80)