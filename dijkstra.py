import heapq


def dijkstra(graph, source):
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    prev = {node: None for node in graph}
    visited = set()

    pq = [(0, source)]

    while pq:
        current_dist, current = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        for neighbor, cost in graph.get(current, {}).items():
            if neighbor in visited:
                continue
            new_dist = current_dist + cost
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                prev[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))

    return distances, prev


def build_routing_table(distances, prev, source):
    routing_table = {}

    for dest in distances:
        if dest == source:
            routing_table[dest] = (source, 0)
            continue
        if distances[dest] == float('inf'):
            routing_table[dest] = ('-', float('inf'))
            continue

        next_hop = dest
        while prev.get(next_hop) != source and prev.get(next_hop) is not None:
            next_hop = prev[next_hop]

        if prev.get(next_hop) is None:
            routing_table[dest] = ('-', float('inf'))
        else:
            routing_table[dest] = (next_hop, distances[dest])

    return routing_table
