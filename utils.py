import os
import csv
import random
from auth import get_twitter_conn_v1, get_twitter_conn_v2
from trend import scrape_and_sort

# Constants
APP_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(APP_DIR, "images")
CONTENT_CSV_PATH = os.path.join(APP_DIR, "content.csv")

# Authenticate with Twitter using your keys
client_v1 = get_twitter_conn_v1()
client_v2 = get_twitter_conn_v2()

trend = scrape_and_sort()

def get_random_content():
    with open(CONTENT_CSV_PATH, 'r', newline='') as csvfile:
        content_data = list(csv.reader(csvfile))
    
    if content_data:
        # Randomly select a row from the CSV containing id and content
        random_row = random.choice(content_data)
        tweet_id, tweet_content = random_row[0], random_row[1]
        return tweet_id, tweet_content
    else:
        print("No content found in the CSV file.")
        return None, None

def get_random_image():
    image_files = os.listdir(IMAGES_DIR)
    if image_files:
        random_image_filename = random.choice(image_files)
        image_path = os.path.join(IMAGES_DIR, random_image_filename)
        return image_path
    else:
        print("No image files found in the 'images' folder.")
        return None

def create_and_post_tweet(client_v1, client_v2):
    tweet_id, tweet_content = get_random_content()
    if tweet_id is None or tweet_content is None:
        print("No more tweets to post.")
        return

    # Modify this part to use the randomly chosen image
    image_path = get_random_image()
    if image_path is not None:
        print(f"API Key: {api_key}")
        print(f"API Secret: {api_secret}")
        print(f"Access Token: {access_token}")
        print(f"Access Token Secret: {access_token_secret}")
        user = client_v1.get_user(screen_name="@atola4u")
        print(f"User's name: {user.name}")

        media = client_v1.simple_upload(filename=image_path)
        media_id = media.media_id

        client_v2.create_tweet(text=tweet_content+"\n"+"\n"+"-----------\n"+trend, media_ids=[media_id])
        print("Tweet posted successfully!")
        # print(tweet_content+"\n"+"\n"+"-----------\n"+trend)

# Call create_and_post_tweet with your Twitter API clients
create_and_post_tweet(client_v1, client_v2)
