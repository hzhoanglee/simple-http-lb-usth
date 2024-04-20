import matplotlib.pyplot as plt
from datetime import datetime

# Initialize dictionary to store counts of requests per second
requests_per_second = {}

# Read the history.log file
with open("history.log", "r") as log_file:
    for line in log_file:
        # Split each line by '|'
        parts = line.strip().split("|")
        if len(parts) == 2:
            # Extract timestamp
            timestamp_str = parts[0]
            # Convert timestamp string to datetime object
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            # Extract second from timestamp
            second = timestamp.replace(microsecond=0)
            # Count requests per second
            requests_per_second[second] = requests_per_second.get(second, 0) + 1

# Extract timestamps and counts
timestamps = list(requests_per_second.keys())
counts = list(requests_per_second.values())

# Plot the chart
plt.figure(figsize=(10, 6))
plt.plot(timestamps, counts, marker='o', linestyle='-')
plt.title('Number of Requests Per Second')
plt.xlabel('Time')
plt.ylabel('Number of Requests')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
