from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from flask import Flask, jsonify

from utils import create_and_post_tweet, client_v1, client_v2

app = Flask(__name__)

# Define a function to run the job
def job():
    now_gmt1 = datetime.now()

    print(f"Job run at {now_gmt1}")

    create_and_post_tweet(client_v1, client_v2)

# Route for the Cyclic API request
@app.route('/api', methods=['GET'])
def api():
    job()  # Run the job immediately
    print("Script executed fro job")
    return jsonify({"message": "Script executed"})

if __name__ == '__main__':
    # Initialize the scheduler
    scheduler = BlockingScheduler()

    # Define the cron expression for scheduling (every hour)
    cron_expression = '0 * * * *'

    # Add the job with the cron expression
    scheduler.add_job(job, 'cron', minute=0)

    # Start the scheduler
    scheduler.start()

    # Start the Flask app
    app.run(host='0.0.0.0', port=8080)
