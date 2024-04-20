import requests
from datetime import datetime

# Define the URL to send requests to
url = "http://localhost:8080"

# Define the number of requests to send
num_requests = 1000

# Define any additional headers or parameters if needed
headers = {
    "User-Agent": "MyScript/1.0"
}

# Open the log file for writing
with open("history.log", "a") as log_file:
    # Loop to send requests
    for i in range(num_requests):
        try:
            # Send GET request
            response = requests.get(url, headers=headers)

            # Get current time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Write to log file
            log_file.write(f"{current_time}|{response.status_code}\n")

            # Print status code and content of response
            print(f"Request {i+1}: Status Code - {response.status_code}, Response - {response.text}")

        except requests.RequestException as e:
            # Print error if request fails
            print(f"Request {i+1}: Failed - {e}")
