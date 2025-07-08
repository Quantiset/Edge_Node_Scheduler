from utils import *
import random
import sys
sys.setrecursionlimit(10**6)

class Request:
    def __init__(self, id, prompt_length, output_length, latency, accuracy):
        self.id = id
        self.prompt_length = prompt_length
        self.output_length = output_length
        self.latency = latency
        self.accuracy = accuracy
        # Calculate bandwidth cost using the formula k_4 * n_i + k_5 * n_i^2
        self.bandwidth_cost = k_4 * output_length + k_5 * output_length**2

class SolutionNode:
    def __init__(self, selected_requests, all_requests, depth=0, parent=None):
        self.selected_requests = selected_requests
        self.all_requests = all_requests  
        self.depth = depth
        self.parent = parent
        self.visited = False
        self.total_latency = sum(req.latency for req in selected_requests)
        self.total_bandwidth_cost = sum(req.bandwidth_cost for req in selected_requests)
   
    def meets_constraints(self, z, max_bandwidth, max_latency):
        return (
            len(self.selected_requests) == z and
            self.total_bandwidth_cost <= max_bandwidth and
            self.total_latency <= max_latency
        )
   
    def __repr__(self):
        return f"SolutionNode(depth={self.depth}, selected_requests={[req.id for req in self.selected_requests]}, visited={self.visited})"

def optimal_tree_search(I, max_bandwidth, max_latency):
    """
    Algorithm 2: Optimal Tree-Search (OT)
    Input: Available request set I
    Output: Optimal subset S* to Problem P2 with added communication constraints
    """
    # Initialize z = 0, d = 0, F_d = ∅, S' = ∅
    S_star = None
    
    # for z = |I|, |I| - 1, ..., 1 do
    for z in range(len(I), 0, -1):
        # Sort I according to τ_i's in descending order (latency descending)
        I_sorted = sorted(I, key=lambda x: x.latency, reverse=True)
        
        # for d = z, z + 1, ..., |I| do
        for d in range(z, len(I) + 1):
            # τ_min ← τ_d; F_d ← the first d - 1 requests in I
            F_d = I_sorted[:d]
            
            # Group F_d by output length
            groups = group_requests_by_length(F_d)
            if not groups:
                continue
                
            # Construct root node v_0 for F_d
            root_node = TreeNode(groups, depth=0, selected_counts=[])
            
            # Call DFS(v_0, d)
            result = DFS(root_node, d, z, groups, max_bandwidth, max_latency)
            if result is not None:
                return result
    
    return None

class TreeNode:
    """Node in the search tree following the paper's structure"""
    def __init__(self, groups, depth=0, selected_counts=None, parent=None):
        self.groups = groups  # Dictionary mapping group index to requests
        self.depth = depth  # N(v) - current depth/group being processed
        self.selected_counts = selected_counts or []  # [v_1, v_2, ..., v_N(v)]
        self.parent = parent
        self.visited = False
        self.children = []
        
        # Calculate accumulated constraints for pruning
        self.accumulated_bandwidth = 0
        self.accumulated_latency = 0
        self.accumulated_memory = 0
        self._calculate_accumulated_values()
    
    def _calculate_accumulated_values(self):
        """Calculate accumulated constraint values along the path"""
        for group_idx, count in enumerate(self.selected_counts, 1):
            if group_idx in self.groups:
                # Select top 'count' requests with smallest bandwidth from this group
                group_requests = self.groups[group_idx]
                sorted_group = sorted(group_requests, key=lambda x: x.bandwidth_cost)
                selected = sorted_group[:count]
                
                self.accumulated_bandwidth += sum(req.bandwidth_cost for req in selected)
                self.accumulated_latency += sum(req.latency for req in selected)
                self.accumulated_memory += sum(req.output_length for req in selected)

def group_requests_by_length(F_d):
    """
    Group requests by output length: F_d = F_{N_1} U F_{N_2} U ... U F_{N_max}
    Returns: Dictionary mapping group index to list of requests
    """
    if not F_d:
        return {}
        
    # Group by output length
    length_groups = {}
    for req in F_d:
        length = req.output_length
        if length not in length_groups:
            length_groups[length] = []
        length_groups[length].append(req)
    
    # Sort lengths and create indexed groups (N_1 = shortest, N_max = longest)
    sorted_lengths = sorted(length_groups.keys())
    indexed_groups = {}
    for i, length in enumerate(sorted_lengths, 1):
        indexed_groups[i] = length_groups[length]
    
    return indexed_groups

def DFS(v_N, d, z, groups, max_bandwidth, max_latency):
    """
    Depth-First Search function following Algorithm 2 pseudocode
    """
    N_v = v_N.depth
    
    # Check if we've reached the target number of requests
    total_selected = sum(v_N.selected_counts)
    
    # if ∑_{k=1}^{N(v)} v_k = d then
    if total_selected == z:
        # Recover the subset S' from v_N
        S_prime = recover_subset_from_node(v_N)
        
        # if S' meets constraints (15b)-(15e) then return S'
        if meets_all_constraints(S_prime, max_bandwidth, max_latency):
            return S_prime
        else:
            # Mark v_N visited and try sibling
            v_N.visited = True
            return try_sibling_nodes(v_N, d, z, groups, max_bandwidth, max_latency)
    
    # elif ∑_{k=1}^{N(v)} v_k < d and N(v) = N then
    elif total_selected < z and N_v == len(groups):
        # Mark v_N and related nodes visited
        mark_node_and_related_visited(v_N)
        # Try parent node
        if v_N.parent is not None:
            return DFS(v_N.parent, d, z, groups, max_bandwidth, max_latency)
    
    # else if ∑_{k=1}^{N(v)} v_k < d and N(v) < N then
    elif total_selected < z and N_v < len(groups):
        # if all child nodes are visited then
        if all_child_nodes_visited(v_N, z, groups):
            if v_N.parent is None:
                return None
            else:
                return DFS(v_N.parent, d, z, groups, max_bandwidth, max_latency)
        else:
            # Create next child node
            next_group = N_v + 1
            if next_group in groups:
                # v_{N(v)+1} ← min{z', |F_{N(v)+1}|}
                z_prime = z - total_selected
                max_from_group = len(groups[next_group])
                next_count = min(z_prime, max_from_group)
                
                # Try from maximum count down to 0 (greedy approach)
                for count in range(next_count, -1, -1):
                    if can_prune_branch(v_N, count, z, groups):
                        continue
                        
                    new_counts = v_N.selected_counts + [count]
                    child_node = TreeNode(groups, depth=next_group, 
                                        selected_counts=new_counts, parent=v_N)
                    v_N.children.append(child_node)
                    
                    result = DFS(child_node, d, z, groups, max_bandwidth, max_latency)
                    if result is not None:
                        return result
    
    return None

def recover_subset_from_node(node):
    """
    Recover the actual subset S' from the tree node path
    """
    S_prime = []
    
    for group_idx, count in enumerate(node.selected_counts, 1):
        if group_idx in node.groups and count > 0:
            # Select top 'count' requests with smallest bandwidth from group
            group_requests = node.groups[group_idx]
            sorted_group = sorted(group_requests, key=lambda x: x.bandwidth_cost)
            S_prime.extend(sorted_group[:count])
    
    return S_prime

def meets_all_constraints(S_prime, max_bandwidth, max_latency):
    """
    Check if subset S' meets all constraints
    """
    if not S_prime:
        return False
    
    total_bandwidth = sum(req.bandwidth_cost for req in S_prime)
    total_latency = sum(req.latency for req in S_prime)
    
    return (total_bandwidth <= max_bandwidth and 
            total_latency <= max_latency)

def try_sibling_nodes(node, d, z, groups, max_bandwidth, max_latency):
    """Try sibling nodes with larger indices"""
    if node.parent is None or not node.selected_counts:
        return None
        
    # Try to modify the last selected count
    parent = node.parent
    last_group = len(node.selected_counts)
    current_count = node.selected_counts[-1]
    
    if last_group in groups:
        max_possible = len(groups[last_group])
        # Try larger counts
        for new_count in range(current_count + 1, max_possible + 1):
            new_counts = node.selected_counts[:-1] + [new_count]
            sibling = TreeNode(groups, depth=node.depth, 
                             selected_counts=new_counts, parent=parent)
            if not sibling.visited:
                result = DFS(sibling, d, z, groups, max_bandwidth, max_latency)
                if result is not None:
                    return result
    
    return None

def mark_node_and_related_visited(node):
    """Mark node and related nodes as visited"""
    node.visited = True

def all_child_nodes_visited(node, z, groups):
    """Check if all possible child nodes have been explored"""
    if node.depth >= len(groups):
        return True
    
    next_group = node.depth + 1
    if next_group not in groups:
        return True
        
    total_selected = sum(node.selected_counts)
    remaining = z - total_selected
    
    return remaining <= 0

def can_prune_branch(node, next_count, z, groups):
    """
    Tree pruning: check if branch can be pruned
    Returns True if branch should be pruned
    """
    total_selected = sum(node.selected_counts) + next_count
    remaining_groups = len(groups) - node.depth - 1
    
    if remaining_groups > 0:
        # Check if remaining groups can provide enough requests
        max_remaining = sum(len(groups[i]) for i in range(node.depth + 2, len(groups) + 1))
        if total_selected + max_remaining < z:
            return True
    
    return False

# Main execution
def paper_2_sol(requests):

    max_bandwidth = 2500000000000
    max_latency = 30000000000
    size = 5000
    requests = [Request(i, random.randint(1, 100), random.randint(1, 10)*10,
                       random.randint(30000, 60000), random.randint(1, 100))
               for i in range(size)]
       
    optimal_solution = optimal_tree_search(requests, max_bandwidth, max_latency)
    if optimal_solution:
        print("Optimal Requests Selected:")
        for req in optimal_solution:
            print(f"Request ID: {req.id}, Prompt Length: {req.prompt_length}, "
                  f"Output Length: {req.output_length}, Latency: {req.latency}, "
                  f"Accuracy: {req.accuracy}, Bandwidth Cost: {req.bandwidth_cost}")
        print(f"Total Requests: {len(optimal_solution)}")
        print(f"Total Bandwidth Cost: {sum(req.bandwidth_cost for req in optimal_solution)}")
        print(f"Total Latency: {sum(req.latency for req in optimal_solution)}")
    else:
        print("No valid solution found.")

if __name__ == "__main__":
    paper_2_sol([])  # Call with an empty list to test the function
    # You can replace the empty list with actual requests to test with real data