package main

import (
	"fmt"
	"gopkg.in/yaml.v3"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"sync"
	"sync/atomic"
	"time"
)

type Server struct {
	URL    *url.URL
	Weight int
}

type ServerConf struct {
	Address string `yaml:"address"`
	Port    int    `yaml:"port"`
	Weight  int    `yaml:"weight"`
}

type Config struct {
	Servers []*ServerConf `yaml:"servers"`
}

var (
	serversArr     []*Server
	servers        = parseConfig()
	serversDefault = []*Server{
		{URL: parseURL("http://localhost:8081"), Weight: 1},
		{URL: parseURL("http://localhost:8082"), Weight: 2},
		{URL: parseURL("http://localhost:8083"), Weight: 3},
	}
	currentServer uint64
	lock          sync.Mutex
	totalWeight   int = getTotalWeight()
)

func parseConfig() []*Server {
	file, err := os.ReadFile("./config.yaml")
	if err != nil {
		return serversDefault
	}

	var config Config
	err = yaml.Unmarshal([]byte(file), &config)
	if err != nil {
		return serversDefault
	}

	for _, server := range config.Servers {
		serversArr = append(serversArr, &Server{
			URL:    parseURL(fmt.Sprintf("http://%s:%d", server.Address, server.Port)),
			Weight: server.Weight,
		})
	}
	// print servers
	for _, server := range serversArr {
		fmt.Println("Server URL:", server.URL, "Server Weight:", server.Weight)
	}
	return serversArr

}

// parseURL is a helper function to parse strings to URL objects
func parseURL(serverURL string) *url.URL {
	parsedURL, err := url.Parse(serverURL)
	if err != nil {
		log.Fatalf("Could not parse server URL: %v", err)
	}
	return parsedURL
}

// getTotalWeight calculates the total weight of all servers.
func getTotalWeight() int {
	total := 0
	for _, server := range servers {
		total += server.Weight
	}
	return total
}

// getNextServerIndex returns the index of the next server to use based on weight.
func getNextServerIndex() int {
	lock.Lock()
	defer lock.Unlock()

	target := atomic.AddUint64(&currentServer, 1) % uint64(totalWeight)
	currentWeight := 0
	for index, server := range servers {
		currentWeight += server.Weight
		if uint64(currentWeight) > target {
			return index
		}
	}
	return 0 // fallback in case of an error
}

// getProxy returns a reverse proxy to the next available server based on the round-robin and weight.
func getProxy() *httputil.ReverseProxy {
	serverIndex := getNextServerIndex()
	var response *httputil.ReverseProxy

	// Try to find an available server
	for i := 0; i < len(servers); i++ {
		url := servers[serverIndex].URL
		fmt.Println("Server index:", serverIndex, "Server URL:", url)

		// Check if the server is available
		client := http.Client{
			Timeout: 5 * time.Second, // Adjust the timeout as needed
		}
		resp, err := client.Get(url.String() + "/health")
		if err == nil && resp.StatusCode == http.StatusOK {
			// Server is available, create a reverse proxy and return
			response = httputil.NewSingleHostReverseProxy(url)
			return response
		}

		// Server is not available, try the next one
		serverIndex = (serverIndex + 1) % len(servers)
	}

	fmt.Println("All servers are down")
	return nil
}

// handleRequestAndRedirect redirects incoming requests to the next server based on the round-robin and weight.
func handleRequestAndRedirect(res http.ResponseWriter, req *http.Request) {
	proxy := getProxy()

	// Setting up a timeout for the request
	proxy.Transport = &http.Transport{
		ResponseHeaderTimeout: time.Second * 10, // Timeout after 10 seconds
	}
	proxy.ServeHTTP(res, req)
}

func main() {
	// Start the load balancer
	http.HandleFunc("/", handleRequestAndRedirect)
	log.Println("Load balancer started, listening on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
