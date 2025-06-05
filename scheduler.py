
# paper variables
k_4 = 1.0
k_5 = 1.0
k_6 = 1.0

class Request:
    def __init__(self, prompt_length, output_length, latency, accuracy):
        self.prompt_length = prompt_length
        self.output_length = output_length
        self.latency = latency
        self.accuracy = accuracy

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
        Request(id=1, bandwidth=10, memory=5, latency=2),
        Request(id=2, bandwidth=20, memory=10, latency=1),
        Request(id=3, bandwidth=15, memory=8, latency=3),
    ]

    optimal_solution = optimal_tree_search(requests, max_bandwidth, max_memory, max_latency)
    if optimal_solution:
        print("Optimal Requests Selected:")
        for req in optimal_solution:
            print(f"Request ID: {req.id}, Bandwidth: {req.bandwidth}, Memory: {req.memory}, Latency: {req.latency}")
    else:
        print("No valid solution found.")