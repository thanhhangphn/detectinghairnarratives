import requests
import csv
import time

def fetch_nyt_search_results(api_key, query, begin_date, end_date, page=0):
    base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {
        'api-key': api_key,
        'q': query,
        'begin_date': begin_date,
        'end_date': end_date,
        'page': page,  # Specify the page number
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'response' in data and 'docs' in data['response']:
            return data['response']['docs']
        else:
            print("No documents found in the response.")
            return None
    else:
        print(f"Error fetching data from the New York Times API. Status Code: {response.status_code}")
        print(response.text)
        return None

def extract_keywords(keywords):
    # Extract keyword values from the 'keywords' field
    # You may need to customize this based on the actual structure of the 'keywords' field
    return [keyword.get('value', '') for keyword in keywords] if keywords else []

def convert_to_csv(articles, csv_filename):
    if not articles:
        print("No data to append to CSV.")
        return

    fields = ['web_url', 'headline', 'pub_date', 'keywords']

    with open(csv_filename, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)

        # Check if the file is empty and write the header if needed
        if csv_file.tell() == 0:
            writer.writeheader()

        for article in articles:
            keywords = extract_keywords(article.get('keywords', []))
            row = {
                'web_url': article.get('web_url', ''),
                'headline': article.get('headline', {}).get('main', ''),
                'pub_date': article.get('pub_date', ''),
                'keywords': ', '.join(keywords),
            }
            writer.writerow(row)

if __name__ == "__main__":
    api_key = 'PDATTNGYbUloNyVQ4GyYrqGpFUtybsNK'
    query = 'african american hair'
    begin_date = '20100101'  # Format: YYYYMMDD
    end_date = '20231212'  # Format: YYYYMMDD
    csv_filename = 'nyt_search_results.csv'

    page = 0
    requests_today = 0

    while requests_today < 500:
        # Make another API request with pagination
        time.sleep(12)
        articles = fetch_nyt_search_results(api_key, query, begin_date, end_date, page)
        print("Make another API request with pagination")
        if articles:
            convert_to_csv(articles, csv_filename)
            requests_today += 1
            page += 1  # Move to the next page for the next iteration

    print("API request limit reached for the day.")
