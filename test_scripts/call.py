import requests

# Define the URL to send requests to
url = "http://localhost:8080"

# Define the number of requests to send
num_requests = 1000

# Define any additional headers or parameters if needed
headers = {
    "User-Agent": "MyScript/1.0"
}

# Loop to send requests
for i in range(num_requests):
    try:
        # Send GET request
        response = requests.get(url, headers=headers)

        # Print status code and content of response
        print(f"Request {i+1}: Status Code - {response.status_code}, Response - {response.text}")

    except requests.RequestException as e:
        # Print error if request fails
        print(f"Request {i+1}: Failed - {e}")
