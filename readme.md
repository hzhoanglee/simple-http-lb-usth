# simple-http-lb-usth

## 1. Introduction
This is a simple HTTP load balancer that distributes incoming HTTP requests to multiple servers.

## 2. Features
- Round-robin load balancing
- Health check
- Configurable server list

## 3. Pre-Installation
### 3.1. Install Go
### 3.2. Install Go packages
```bash
go mod tidy
```
### 3.3. Config server list
Edit `config.yaml` file to add server list
```yaml
servers:
  - address: localhost
    port: 8081
    weight: 1
  - address: localhost
    port: 8082
    weight: 2
  - address: localhost
    port: 8083
    weight: 3
```

### 3.4 For testing
Install Docker and Docker Compose

### 3.5 For analyzing
Install python

## 4. Usage
### 3.1. Build main.go
```bash
go build -o main main.go
```

### 3.2. Run main.go
```bash
./main
```

### 3.3. Run docker cluster
Open new terminal and run
```bash
cd docker && docker-compose up
```

### 3.4. Test with 1000 requests
Open new terminal and run
```bash
cd test_scripts && python call.py && cd ../
```

### 3.5. Make test log for analyzing
Please delete `docker/data.log` before running the test for the correct result
```bash
> docker/data.log
```
Send 1000 requests with 3 servers up
```bash
python test_scripts/call.py && cp docker/data.log docker/3servers.log && > docker/data.log
```
Now, you can shut down 1 server in docker and send 1000 requests again with 2 servers up
```bash
python test_scripts/call.py && cp docker/data.log docker/2servers.log && > docker/data.log
```
Now, shut down 1 more server in docker and send 1000 requests again with 1 server up
```bash
python test_scripts/call.py && cp docker/data.log docker/1server.log && > docker/data.log
```

## 5. Analyzing
```bash
cd test_scripts && python analyze.py
```

Example output:
```
Analyze for all 3 servers up:
CLIENT 0: 172.20.0.1
172.20.0.3: 334 requests
172.20.0.2: 500 requests
172.20.0.4: 166 requests
===================

Analyze for all 2 servers up:
CLIENT 0: 172.20.0.1
172.20.0.2: 499 requests
172.20.0.3: 501 requests
===================

Analyze for all 1 servers up:
CLIENT 0: 172.20.0.1
172.20.0.3: 1000 requests
===================
```

## 6. Conclusion
The load balancer distributes incoming HTTP requests to multiple servers based on the round-robin algorithm. The health check feature is implemented to check the status of the servers. The server list is configurable in the `config.yaml` file. The load balancer is tested with 1000 requests and analyzed for different scenarios. The result shows that the load balancer distributes the requests based on the weight of the servers. The load balancer is working as expected and can be used in a production environment.