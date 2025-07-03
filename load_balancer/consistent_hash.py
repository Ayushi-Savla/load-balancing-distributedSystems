import hashlib

class ConsistentHash:
    def __init__(self, num_slots=512, replicas=9):
        self.num_slots = num_slots
        self.replicas = replicas
        self.hash_ring = dict()
        self.sorted_keys = []
        self.server_map = dict()

    def _hash(self, key):
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16) % self.num_slots

    def add_server(self, server_id):
        for i in range(self.replicas):
            virtual_id = f"{server_id}#{i}"
            key = self._hash(virtual_id)
            while key in self.hash_ring:
                key = (key + 1) % self.num_slots
            self.hash_ring[key] = server_id
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_server(self, server_id):
        self.hash_ring = {k: v for k, v in self.hash_ring.items() if v != server_id}
        self.sorted_keys = sorted(self.hash_ring.keys())

    def get_server(self, client_id):
        key = self._hash(client_id)
        for server_key in self.sorted_keys:
            if key <= server_key:
                return self.hash_ring[server_key]
        return self.hash_ring[self.sorted_keys[0]]
