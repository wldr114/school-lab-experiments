import threading
import queue
import time

from lsp import LinkStatePacket
from dijkstra import dijkstra, build_routing_table


class Router(threading.Thread):

    def __init__(self, node_id, topology, msg_queues, simulator):
        super().__init__(daemon=True)
        self.node_id = node_id
        self.topology = topology
        self.msg_queues = msg_queues
        self.simulator = simulator

        self.lsdb = {}
        self.routing_table = {}
        self.own_seq_num = 0
        self.global_graph = {}
        self.running = True
        self.routing_table_updated = threading.Event()

    def generate_own_lsp(self):
        neighbors = self.topology.get_all_neighbors_with_cost(self.node_id)
        self.own_seq_num += 1
        lsp = LinkStatePacket(self.node_id, neighbors, sequence_num=self.own_seq_num)
        return lsp

    def flood_lsp(self, lsp):
        neighbors = self.topology.get_neighbors(self.node_id)
        for neighbor_id in neighbors:
            if neighbor_id in self.msg_queues:
                copied = LinkStatePacket(
                    lsp.origin_id,
                    list(lsp.neighbors),
                    sequence_num=lsp.sequence_num
                )
                copied.ttl = lsp.ttl
                try:
                    self.msg_queues[neighbor_id].put(copied, timeout=0.1)
                except queue.Full:
                    pass

    def process_lsp(self, lsp):
        if not lsp.decrement_ttl():
            return

        origin = lsp.origin_id
        if origin == self.node_id:
            return

        if origin in self.lsdb:
            if lsp.sequence_num <= self.lsdb[origin].sequence_num:
                return

        self.lsdb[origin] = lsp
        self._rebuild_global_graph()
        self.flood_lsp(lsp)

    def _rebuild_global_graph(self):
        new_graph = {}
        for origin, lsp in self.lsdb.items():
            if origin not in new_graph:
                new_graph[origin] = {}
            for neighbor, cost in lsp.neighbors:
                new_graph[origin][neighbor] = cost
                if neighbor not in new_graph:
                    new_graph[neighbor] = {}
                new_graph[neighbor][origin] = cost

        for node in self.topology.nodes:
            if node not in new_graph:
                new_graph[node] = {}

        for node in self.topology.nodes:
            for neighbor, cost in self.topology.get_neighbors(node).items():
                new_graph[node][neighbor] = cost

        self.global_graph = new_graph

    def compute_routing_table(self):
        graph = {}
        for node in self.topology.nodes:
            graph[node] = self.topology.get_neighbors(node)

        distances, prev = dijkstra(graph, self.node_id)
        self.routing_table = build_routing_table(distances, prev, self.node_id)
        self.routing_table_updated.set()
        self.routing_table_updated.clear()

    def run(self):
        own_lsp = self.generate_own_lsp()
        self.lsdb[self.node_id] = own_lsp
        self.flood_lsp(own_lsp)
        self._rebuild_global_graph()
        self.compute_routing_table()

        update_timer = 0
        while self.running:
            try:
                msg = self.msg_queues[self.node_id].get(timeout=0.5)
                if isinstance(msg, LinkStatePacket):
                    self.process_lsp(msg)
                    self.compute_routing_table()
                elif isinstance(msg, str) and msg == "HELLO":
                    own_lsp = self.generate_own_lsp()
                    self.lsdb[self.node_id] = own_lsp
                    self.flood_lsp(own_lsp)
                elif isinstance(msg, str) and msg == "UPDATE":
                    own_lsp = self.generate_own_lsp()
                    self.lsdb[self.node_id] = own_lsp
                    self.flood_lsp(own_lsp)
                    self._rebuild_global_graph()
                    self.compute_routing_table()
            except queue.Empty:
                pass

            update_timer += 1
            if update_timer >= 5:
                self.compute_routing_table()
                update_timer = 0

    def stop(self):
        self.running = False


class NetworkSimulator:

    def __init__(self, topology):
        self.topology = topology
        self.msg_queues = {}
        self.routers = {}
        self._lock = threading.Lock()

        for node_id in topology.nodes:
            self.msg_queues[node_id] = queue.Queue(maxsize=100)

    def start(self):
        for node_id in self.topology.nodes:
            router = Router(node_id, self.topology, self.msg_queues, self)
            self.routers[node_id] = router
            router.start()

        time.sleep(1.0)

    def stop(self):
        for router in self.routers.values():
            router.stop()
        for router in self.routers.values():
            router.join(timeout=2)

    def trigger_update(self, node_id=None):
        if node_id:
            if node_id in self.msg_queues:
                self.msg_queues[node_id].put("UPDATE")
        else:
            for nid in self.topology.nodes:
                if nid in self.msg_queues:
                    self.msg_queues[nid].put("UPDATE")

        time.sleep(1.0)

    def get_routing_tables(self):
        return {nid: dict(router.routing_table)
                for nid, router in self.routers.items()}

    def get_lsdb(self, node_id):
        if node_id in self.routers:
            return dict(self.routers[node_id].lsdb)
        return {}
