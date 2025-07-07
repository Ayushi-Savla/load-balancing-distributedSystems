import hashlib  # Used for generating hash values

class ConsistentHash:
    def __init__(self, num_slots=512, replicas=9):
        # Total number of slots in the hash ring (circular)
        self.num_slots = num_slots

        # Number of virtual replicas per physical server (improves load distribution)
        self.replicas = replicas

        # Dictionary to map slot key to server ID
        self.hash_ring = dict()

        # Sorted list of slot keys (used to find next closest server in clockwise direction)
        self.sorted_keys = []

        # Optional map from server_id to list of keys (not used directly here but useful in expansions)
        self.server_map = dict()

    # Hash function to map input keys (client ID or virtual server ID) to a slot index
    def _hash(self, key):
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16) % self.num_slots

    # Add a server to the hash ring with its virtual replicas
    def add_server(self, server_id):
        for i in range(self.replicas):
            virtual_id = f"{server_id}#{i}"  # Create virtual server ID
            key = self._hash(virtual_id)    # Hash the virtual ID to get a slot

            # Resolve collision using linear probing
            while key in self.hash_ring:
                key = (key + 1) % self.num_slots

            # Map the key to the server
            self.hash_ring[key] = server_id
            self.sorted_keys.append(key)

        # Maintain the sorted keys list
        self.sorted_keys.sort()

    # Remove all virtual nodes of a server from the hash ring
    def remove_server(self, server_id):
        self.hash_ring = {k: v for k, v in self.hash_ring.items() if v != server_id}
        self.sorted_keys = sorted(self.hash_ring.keys())

    # Get the server responsible for a given client ID (hash lookup + clockwise search)
    def get_server(self, client_id):
        key = self._hash(client_id)  # Hash the client ID to get its slot

        for k in self.sorted_keys:
            if key <= k:
                return self.hash_ring[k]  # Return the first server key greater than or equal to hash

        # If not found (wrap around to start of ring)
        return self.hash_ring[self.sorted_keys[0]] if self.sorted_keys else None
