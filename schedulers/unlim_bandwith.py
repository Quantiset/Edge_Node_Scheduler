from utils import *
from avl import AVLTree
import random

requests: list[Request] = [
    Request(1, 6, 10, 5, 2),
    Request(2, 9, 8, 3, 1),
    Request(3, 2, 12, 6, 3),
    Request(4, 5, 7, 2, 1),
]
random.seed(87)  # For reproducibility
for i in range(600):
    requests.append(Request(i+5, random.randint(1, 100), random.randint(1, 100), random.randint(30000, 60000), random.randint(1, 100)))

def is_valid(requests):
    t_min = min(req.latency for req in requests)
    tau_min = t_min
    total_bandwidth = 0
    total_output = 0
    for req in requests:
        total_bandwidth += req.get_bandwidth()
        total_output += req.output_length
        if total_bandwidth > tau_min:  
            return False
        if total_output > k_6:
            return False
    return True

#O(n^3 log n) solution
def paper_1_sol(reqs: list[Request]):
    reqs.sort(key=lambda x: x.latency, reverse=True)
    for z in range(len(reqs), 0, -1):
        for d in range(z, len(reqs) + 1):
            f_d = reqs[:d]
            f_d.sort(key=lambda x: x.output_length, reverse=True)
            s = f_d[:z]
            if is_valid(s):
                return s

# O(n log^2 n) solution
def opt_sol(reqs: list[Request]):

    best_solution = []
    best_solution_bandwidth = 0

    highest_output_length = 0
    output_len_tree = AVLTree()
    reqs.sort(key=lambda x: x.latency, reverse=True)
    
    smallest_output = 999999999999
    for request in reqs:
        tau_min = request.latency
        highest_output_length = max(highest_output_length, request.output_length)

        # log N nodes w.h.p.
        if True or (request.output_length < smallest_output or request == reqs[-1]) and is_valid([request]):
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
            
            print()
            # if mid != highest_output_length:
            #     return (output_len_tree.get_all_less_than(mid))
        
        output_len_tree.insert(request)
    
    return best_solution


# print(paper_1_sol(requests), len(paper_1_sol(requests)))
print(opt_sol(requests), len(opt_sol(requests)))