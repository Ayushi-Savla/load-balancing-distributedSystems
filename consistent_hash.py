import hashlib
import bisect
import math

class ConsistentHashRing:
    def __init__(self, servers=None, replicas=9, slots=512):
        self.replicas = replicas  # K
        self.slots = slots  # M
        self.ring = dict()
        self.sorted_keys = []
        self.server_map = {}

        if servers:
            for server in servers:
                self.add_server(server)

    def _hash(self, key):
        # H(i) = i^2 + 2i + 17
        return int(hashlib.sha256(key.encode()).hexdigest(), 16) % self.slots

    def _virtual_hash(self, sid, vid):
        # Φ(i,j) = i^2 + j + 2j + 25 (string inputs here)
        key = f"{sid}-{vid}"
        return self._hash(key)

    def add_server(self, server_id):
        for v in range(self.replicas):
            h = self._virtual_hash(server_id, v)
            self.ring[h] = server_id
            bisect.insort(self.sorted_keys, h)
        self.server_map[server_id] = True

    def remove_server(self, server_id):
        for v in range(self.replicas):
            h = self._virtual_hash(server_id, v)
            if h in self.ring:
                del self.ring[h]
                self.sorted_keys.remove(h)
        if server_id in self.server_map:
            del self.server_map[server_id]

    def get_server(self, key):
        h = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, h) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]

    def get_all_servers(self):
        return list(self.server_map.keys())
