from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from flask import Flask, jsonify

from utils import create_and_post_tweet, client_v1, client_v2

app = Flask(__name__)

# Define a function to run the job
def job():
    try:
        now_gmt1 = datetime.now()
        print(f"Job run at {now_gmt1}")

        # Add error handling for create_and_post_tweet
        create_and_post_tweet(client_v1, client_v2)
    except Exception as e:
        print(f"Error in job: {e}")

#return index to avoid error
@app.route('/', methods=['GET', 'POST'])
def index():
    # HTML content as a string
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Report Page</title>
    </head>
    <body>
        <h1>Hello, Tweet</h1>
        <p>The bot is still active and running.</p>
    </body>
    </html>
    """    
    return html_content


# Route for the Cyclic API request
@app.route('/api', methods=['GET'])
def api():
    try:
        # Call the job function
        job()
        print("Script executed from job")
        return jsonify({"message": "Script executed successfully"})
    except Exception as e:
        print(f"Error in API route: {e}")
        return jsonify({"error": "An error occurred"}), 500  # Return a 500 error response

if __name__ == '__main__':
    # Initialize the scheduler
    # scheduler = BlockingScheduler()

    # Define the cron expression for scheduling (every hour)
    # cron_expression = '0 * * * *'

    # Add the job with the cron expression
    # scheduler.add_job(job, 'cron', minute=0)

    # Start the scheduler
    # scheduler.start()

    # Start the Flask app on a dynamic port assigned by Cyclic
    app.run(host='0.0.0.0', port=3000)  # Use 0.0.0.0 to listen on all available network interfaces
