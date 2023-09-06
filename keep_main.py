import os
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from utils import create_and_post_tweet, client_v1, client_v2

# Set the time zone to GMT+1 (Central European Time, CET)
# You can adjust the time zone as needed
os.environ['TZ'] = 'Europe/Amsterdam'

# List of specific times when you want the tweet to be posted (in GMT+1)
post_times_gmt1 = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0), (20, 0), (21, 0), (22, 0), (23, 0)]

def job():
    # Get the current time in GMT+1
    now_gmt1 = datetime.now()

    print(f"Job run at {now_gmt1}")

    # Check if the current time falls within a 60-minute interval of any of the post_times_gmt1
    for post_time_hour, post_time_minute in post_times_gmt1:
        if now_gmt1.hour == post_time_hour and now_gmt1.minute == post_time_minute:
            # If it's within the specified interval, post the tweet
            create_and_post_tweet(client_v1, client_v2)

if __name__ == '__main__':
    # Initialize the scheduler
    scheduler = BlockingScheduler()

    # Schedule the job to run every 60 minutes
    scheduler.add_job(job, 'interval', minutes=1)

    # Start the scheduler
    scheduler.start()
