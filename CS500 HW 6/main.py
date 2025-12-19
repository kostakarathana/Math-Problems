import heapq


class Node:
    def __init__(self, val):
        self.val = val
        self.outgoing = []
        self.incoming = []

    def __repr__(self):
        return str(self.val)


def dijkstra_with_tracking(root, all_nodes):
    # Initialize distances
    distances = {node: float('inf') for node in all_nodes.values()}
    distances[root] = 0

    # Priority Queue: (distance, node_val)
    pq = [(0, root.val)]

    # List to track the order nodes are popped/finalized
    finalization_order = []

    while pq:
        current_dist, current_val = heapq.heappop(pq)
        current_node = all_nodes[current_val]

        # Check for stale entries (if we found a faster way to this node already)
        if current_dist > distances[current_node]:
            continue

        # Record this node as being finalized
        finalization_order.append(current_node.val)

        # Explore neighbors
        for neighbor, weight in current_node.outgoing:
            distance = current_dist + weight

            # Relaxation
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor.val))

    return distances, finalization_order


# --- Graph Setup ---
nodes = {i: Node(i) for i in range(6)}


def add_edge(src_val, dest_val, weight):
    src = nodes[src_val]
    dest = nodes[dest_val]
    src.outgoing.append((dest, weight))
    dest.incoming.append((src, weight))


add_edge(0, 1, 1)
add_edge(0, 2, 3)
add_edge(0, 3, 5)
add_edge(0, 4, 7)
add_edge(0, 5, 9)
add_edge(1, 2, 1)
add_edge(2, 1, 1)
add_edge(2, 3, 1)
add_edge(3, 2, 1)
add_edge(3, 4, 1)
add_edge(4, 3, 1)
add_edge(5, 4, -13)

root = nodes[0]

# --- Execution and Print ---
if __name__ == "__main__":
    final_distances, order = dijkstra_with_tracking(root, nodes)

    print("Order in which nodes are finalized:")
    print(order)

    print("\nDistances returned by Dijkstra's algorithm:")
    # Formatting simply as requested
    for node_val in sorted([n.val for n in final_distances]):
        node = nodes[node_val]
        print(f"Node {node}: {final_distances[node]}")