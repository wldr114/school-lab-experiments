import json
import os


class Topology:

    def __init__(self):
        self.graph = {}
        self.nodes = []

    @classmethod
    def from_file(cls, filepath):
        topo = cls()
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"拓扑文件不存在: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        topo.nodes = list(data.get("nodes", []))

        for node in topo.nodes:
            topo.graph[node] = {}

        for edge in data.get("edges", []):
            u = edge["from"]
            v = edge["to"]
            cost = edge["cost"]
            if u in topo.graph and v in topo.graph:
                topo.graph[u][v] = cost
                topo.graph[v][u] = cost

        return topo

    def to_file(self, filepath):
        edges = []
        seen = set()
        for u in self.graph:
            for v, cost in self.graph[u].items():
                edge_key = tuple(sorted([u, v]))
                if edge_key not in seen:
                    seen.add(edge_key)
                    edges.append({"from": u, "to": v, "cost": cost})

        data = {
            "nodes": self.nodes,
            "edges": edges
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_neighbors(self, node_id):
        return dict(self.graph.get(node_id, {}))

    def get_all_neighbors_with_cost(self, node_id):
        return list(self.graph.get(node_id, {}).items())

    def update_edge(self, u, v, cost):
        if u in self.graph and v in self.graph:
            self.graph[u][v] = cost
            self.graph[v][u] = cost
            return True
        return False

    def add_edge(self, u, v, cost):
        if u not in self.graph:
            self.graph[u] = {}
            if u not in self.nodes:
                self.nodes.append(u)
        if v not in self.graph:
            self.graph[v] = {}
            if v not in self.nodes:
                self.nodes.append(v)
        self.graph[u][v] = cost
        self.graph[v][u] = cost

    def remove_edge(self, u, v):
        if u in self.graph and v in self.graph[u]:
            del self.graph[u][v]
            del self.graph[v][u]
            return True
        return False

    def add_node(self, node_id):
        if node_id not in self.graph:
            self.graph[node_id] = {}
            self.nodes.append(node_id)

    def remove_node(self, node_id):
        if node_id in self.graph:
            for neighbor in list(self.graph[node_id].keys()):
                del self.graph[neighbor][node_id]
            del self.graph[node_id]
            self.nodes.remove(node_id)
