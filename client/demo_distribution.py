import matplotlib.pyplot as plt
import random
import pandas as pd
from collections import defaultdict

# A-1: Simulate 10,000 client requests with N=3 servers
def simulate_requests(n_servers=3, n_requests=10000, seed=42):
    random.seed(seed)
    result = defaultdict(int)
    for i in range(n_requests):
        client_id = f"client_{i}"
        selected_server = hash(client_id) % n_servers
        result[f"Server{selected_server+1}"] += 1
    return result

# A-2: Test scalability by increasing N from 2 to 6 (FIXED range)
def simulate_scaling_test(start=2, end=6, n_requests=10000):
    results = []
    for n in range(start, end + 1):  # FIXED: include end value
        result = simulate_requests(n_servers=n, n_requests=n_requests)
        average = sum(result.values()) / len(result)
        results.append((n, average, result))
    return results

# ---- Run Simulations ----
a1_data = simulate_requests(n_servers=3)
a2_data = simulate_scaling_test()

# ---- A-1: Bar Chart of Server Load ----
plt.figure()
plt.bar(a1_data.keys(), a1_data.values())
plt.title("A-1: Load Distribution with N=3 Servers")
plt.xlabel("Server")
plt.ylabel("Number of Requests")
plt.grid(True)
plt.tight_layout()
plt.savefig("a1_load_distribution.png")
plt.show()

# ---- A-2: Line Chart of Average Requests per Server ----
plt.figure()
plt.plot([x[0] for x in a2_data], [x[1] for x in a2_data], marker='o')
plt.title("A-2: Average Load vs Number of Servers")
plt.xlabel("Number of Servers (N)")
plt.ylabel("Average Requests per Server")
plt.grid(True)
plt.tight_layout()
plt.savefig("a2_scalability.png")
plt.show()

# ---- A-1 Table ----
a1_df = pd.DataFrame.from_dict(a1_data, orient='index', columns=['Request Count'])
a1_df.index.name = 'Server'
print("\n📊 A-1: Load Distribution Table (N=3 servers):")
print(a1_df)

# ---- A-2 Summary Table ----
a2_summary = pd.DataFrame([(x[0], x[1]) for x in a2_data], columns=['Servers (N)', 'Average Requests per Server'])
print("\n📈 A-2: Scalability Results Table:")
print(a2_summary)
