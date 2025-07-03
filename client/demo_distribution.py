import requests
from collections import Counter
import matplotlib.pyplot as plt
import time

# Make 1000 requests to the load balancer's /home endpoint
results = []
for _ in range(1000):
    try:
        response = requests.get("http://localhost:5000/home")
        if response.status_code == 200:
            msg = response.json().get("message", "")
            server = msg.split(":")[-1].strip()
            results.append(server)
        else:
            results.append("Error")
    except Exception as e:
        print(f"Request failed: {e}")
        results.append("Exception")
    time.sleep(0.01)  # slight delay to avoid flooding

# Count how many requests each server received
counts = Counter(results)

# Print results to console
print("\nRequest distribution:")
for server, count in counts.items():
    print(f"{server}: {count}")

# Plot the results
plt.figure(figsize=(8, 5))
plt.bar(counts.keys(), counts.values(), color='skyblue')
plt.title("Request Distribution Across Servers")
plt.xlabel("Server")
plt.ylabel("Number of Requests")
plt.tight_layout()
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.show()