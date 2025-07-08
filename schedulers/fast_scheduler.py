
from utils import *
from avl import AVLTree
import random

# O(n log^2 n) solution
def opt_sol(reqs: list[Request]):

    last_reqs = len(reqs) + 1
    best_solution = []
    best_solution_bandwidth = 0

    highest_output_length = 0
    output_len_tree = AVLTree()
    reqs.sort(key=lambda x: x.latency, reverse=True)
    
    smallest_output = 999999999999
    for request in reqs:

        print(f"Remaining requests: {len(best_solution)}", len(best_solution)-last_reqs)
        last_reqs = len(best_solution)

        tau_min = request.latency
        highest_output_length = max(highest_output_length, request.output_length)
        output_len_tree.insert(request)

        # log N nodes w.h.p.
        if True or (request.output_length < smallest_output or request == reqs[-1]):
            smallest_output = request.output_length
            
            lo = 0
            hi = highest_output_length + 1
            mid = (lo + hi) // 2
            while lo < hi:
                mid = (lo + hi) // 2
                if output_len_tree.get_bandwidth_sum_total_less_than(Request.get_bandwidth_from_output_length(mid)) < tau_min:
                    lo = mid + 1
                else:
                    hi = mid
            
            if mid != highest_output_length:
                total_bandwidth = output_len_tree.get_bandwidth_sum_total_less_than(Request.get_bandwidth_from_output_length(mid-1))
                output_set = output_len_tree.get_all_less_than(mid)
                if total_bandwidth <= tau_min and len(output_set) > len(best_solution):#total_bandwidth > best_solution_bandwidth:
                    best_solution_bandwidth = total_bandwidth
                    best_solution = output_set
                    # print(best_solution)
    
    # print(best_solution_tau_min, best_solution_bandwidth)
    return best_solution

if __name__ == "__main__":
    size = 600
    requests = [Request(i, random.randint(1, 100), random.randint(1, 100), random.randint(30000, 60000), random.randint(1, 100)) for i in range(size)]
    opt_sol(requests)