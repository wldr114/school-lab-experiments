import time


class LinkStatePacket:

    def __init__(self, origin_id, neighbors, sequence_num=None):
        self.origin_id = origin_id
        self.sequence_num = sequence_num if sequence_num is not None else int(time.time() * 1000)
        self.neighbors = list(neighbors)
        self.ttl = 64

    def decrement_ttl(self):
        self.ttl -= 1
        return self.ttl > 0

    def __repr__(self):
        return (f"LSP(origin={self.origin_id}, seq={self.sequence_num}, "
                f"neighbors={self.neighbors}, ttl={self.ttl})")
