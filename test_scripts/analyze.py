def analyze_log(log_file):
    # Dictionary to store client IPs and their corresponding server requests
    client_requests = {}

    # Read the log file
    with open(log_file, 'r') as f:
        lines = f.readlines()

    # Process each line in the log file
    for line in lines:
        # Split the line into components
        server_ip, client_ip, _ = line.strip().split(',')

        # Add client IP to the dictionary if not already present
        if client_ip not in client_requests:
            client_requests[client_ip] = {}

        # Increment the request count for the corresponding server IP
        if server_ip not in client_requests[client_ip]:
            client_requests[client_ip][server_ip] = 1
        else:
            client_requests[client_ip][server_ip] += 1

    # Generate the analysis output
    output = ""
    for i, (client_ip, requests) in enumerate(client_requests.items()):
        output += f"CLIENT {i}: {client_ip}\n"
        for server_ip, count in requests.items():
            output += f"{server_ip}: {count} requests\n"
        output += "===================\n"

    return output

# Example usage
print("Analyze for all 3 servers up:")
log_file = '../docker/3servers.log'
analysis_result = analyze_log(log_file)
print(analysis_result)

print("Analyze for all 2 servers up:")
log_file = '../docker/2servers.log'
analysis_result = analyze_log(log_file)
print(analysis_result)

print("Analyze for all 1 servers up:")
log_file = '../docker/1server.log'
analysis_result = analyze_log(log_file)
print(analysis_result)