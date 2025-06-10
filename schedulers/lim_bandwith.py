from utils import *

class SolutionNode:
    def __init__(self, requests, depth=0):
        self.requests = requests
        self.visited = False
        self.parent = None
        self.children = []
        self.depth = depth

def recover_path(node):
    path = []
    while node:
        path.append(node)
        node = node.parent
    return path[::-1]

def dfs(node, depth, max_bandwidth, max_memory, max_latency):
    if node is None or node.visited:
        return None
    
    path = recover_path(node) # generating path from root to curr node -- does on each node to preserve memory w/ networking apps
    if len(path) == depth:
        total_bandwidth = 0
        for node in path:
            for req in node.requests:
                total_bandwidth += req.output_length * k_4 + req.output_length * req.output_length * k_5
        if total_bandwidth <= max_bandwidth:
            return node
        return None
    
    node.visited = True
    for child in node.children:
        if not child.visited:
            child.parent = node
            result = dfs(child, depth, max_bandwidth, max_memory, max_latency)
            if result:
                return result
    return None

def optimal_tree_search(requests, max_bandwidth, max_memory, max_latency):
    requests.sort(key=lambda x: x.latency, reverse=True)
    for z in range(len(requests), 0, -1):
        for d in range(z, len(requests)+1):
            f_d = requests[:d]
            root = SolutionNode(f_d, d)
            sol = dfs(root, d, max_bandwidth, max_memory, max_latency)
            if sol:
                return recover_path(sol)
    return None

if __name__ == "__main__":

    max_bandwidth = 25
    max_memory = 15
    max_latency = 3
    requests = [
        Request(id=1, prompt_length=5, output_length=3, latency=1, accuracy=0.9),
        Request(id=2, prompt_length=4, output_length=2, latency=2, accuracy=0.85),
        Request(id=3, prompt_length=6, output_length=4, latency=1, accuracy=0.95),
        Request(id=4, prompt_length=3, output_length=1, latency=3, accuracy=0.8),
        Request(id=5, prompt_length=7, output_length=5, latency=2, accuracy=0.9)
    ]

    optimal_solution = optimal_tree_search(requests, max_bandwidth, max_memory, max_latency)
    if optimal_solution:
        print("Optimal Requests Selected:")
        for req in optimal_solution:
            print(f"Request ID: {req.id}, Prompt Length: {req.prompt_length}, Output Length: {req.output_length}, Latency: {req.latency}, Accuracy: {req.accuracy}")
        print(f"Total Requests: {len(optimal_solution)}")
    else:
        print("No valid solution found.")