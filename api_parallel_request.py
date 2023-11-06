import threading
import time
import requests
import json
import numpy as np

# Define the API endpoint and request method
api_url = "https://example.com/api"
http_method = "GET"  # Change to "POST" if needed
payload = {}  # Define the payload if using POST

# Number of threads
num_threads = 10

# Total number of API calls to make
total_api_calls = 1000000

# Number of calls per thread
calls_per_thread = total_api_calls // num_threads

# List to store API response times
response_times = []

# List to store percentile data for logging
percentile_data = []

# Function to make API requests
def make_api_requests(thread_num):
    thread_response_times = []
    for i in range(calls_per_thread):
        start_time = time.time()
        
        if http_method == "GET":
            response = requests.get(api_url)
        elif http_method == "POST":
            response = requests.post(api_url, json=payload)
        else:
            print("Unsupported HTTP method.")
            return
        
        end_time = time.time()
        response_time = end_time - start_time

        # Check the response status code
        if response.status_code == 200:
            thread_response_times.append(response_time)
        else:
            print(f"Thread {thread_num}: API call failed with status code {response.status_code}")

        # After every 10,000 requests, calculate and add percentiles data
        if (i + 1) % 10000 == 0:
            calculate_percentiles(thread_response_times, i + 1)

    response_times.extend(thread_response_times)
    print(f"Thread {thread_num}: Made {calls_per_thread} API calls")

def calculate_percentiles(response_times, processed_requests):
    if response_times:
        percentiles = np.percentile(response_times, [90, 95, 99])
        percentile_data.append((processed_requests, percentiles[0], percentiles[1], percentiles[2]))

# Create and start threads
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=make_api_requests, args=(i,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Calculate and print the average response time
average_response_time = sum(response_times) / len(response_times)
print(f"Average API response time for {num_threads} threads = {average_response_time:.2f} seconds")

# Print the percentile data as a single row for logging
if percentile_data:
    processed_requests, p90, p95, p99 = zip(*percentile_data)
    print(f"Processed {processed_requests[-1]} requests - 90th percentile: {p90[-1]:.2f}, 95th percentile: {p95[-1]:.2f}, 99th percentile: {p99[-1]:.2f} seconds")
