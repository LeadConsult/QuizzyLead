import csv
import requests
from bs4 import BeautifulSoup

# Define the scraping function
def scrape_and_sort():
    url = 'https://trends24.in/nigeria/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Process scraped data and limit content to 100 characters
        trends = []
        trend_elements = soup.find_all('div', class_='trend-card')[:2]

        for trend_element in trend_elements:
            ol_element = trend_element.find('ol', class_='trend-card__list')
            trend_items = ol_element.find_all('li')

            for trend_item in trend_items:
                anchor_element = trend_item.find('a')
                tweet_count_element = trend_item.find('span', class_='tweet-count')

                if anchor_element and tweet_count_element:
                    trend_text = anchor_element.text
                    tweet_count = tweet_count_element.text

                    # Limit content to 100 characters
                    trend_text = trend_text[:100]

                    trends.append({'trendText': trend_text, 'tweetCount': tweet_count})

        # Sort the data by tweet count in descending order (parsed as integers)
        trends.sort(key=lambda x: int(x['tweetCount'].replace('K', '')), reverse=True)

        # Initialize a set to track unique trendText values
        unique_trend_text = set()

        # Filter and deduplicate the data array
        deduplicated_data = []
        for item in trends:
            if item['trendText'] not in unique_trend_text:
                deduplicated_data.append(item)
                unique_trend_text.add(item['trendText'])

        # Format deduplicated_data as a single string separated by "|"
        formatted_data = "|".join(item['trendText'] for item in deduplicated_data)

        # Limit the content to 100 characters
        formatted_data = formatted_data[:100]

        # Write the formatted data to CSV file (overwrite)
        # with open('temp_content.csv', 'w', newline='', encoding='utf-8') as csvfile:
        #     fieldnames = ['trendText']
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     # writer.writeheader()
        #     writer.writerow({'trendText': formatted_data})

        # print('Data scraped, sorted, and written to CSV successfully')
        # print(formatted_data)

    return formatted_data

# Call the scraping and sorting function
# print(scrape_and_sort())
