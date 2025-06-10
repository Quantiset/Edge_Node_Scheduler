
from utils import *
from avl import AVLTree
import random

def is_valid(requests):
    t_min = min(req.latency for req in requests)
    tau_min = t_min
    total_bandwidth = 0
    total_output = 0
    for req in requests:
        total_bandwidth += req.get_bandwidth()
        total_output += req.output_length
        if total_bandwidth > tau_min:  
            return 0
        # if total_output > k_6:
        #     return 0
    return total_bandwidth

#O(n^3 log n) solution
def paper_1_sol(reqs: list[Request]):
    reqs.sort(key=lambda x: x.latency, reverse=True)
    for z in range(len(reqs), 0, -1):
        for d in range(z, len(reqs) + 1):
            f_d = reqs[:d]
            f_d.sort(key=lambda x: x.output_length, reverse=True)
            s = f_d[:z]
            bandwidth = is_valid(s)
            if bandwidth:
                # print(min(req.latency for req in s), bandwidth)
                return s

# O(n log^2 n) solution
def opt_sol(reqs: list[Request]):

    best_solution = []
    best_solution_bandwidth = 0
    best_solution_tau_min = 0

    highest_output_length = 0
    output_len_tree = AVLTree()
    reqs.sort(key=lambda x: x.latency, reverse=True)
    
    smallest_output = 999999999999
    for request in reqs:
        tau_min = request.latency
        highest_output_length = max(highest_output_length, request.output_length)
        output_len_tree.insert(request)

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
            
            if mid != highest_output_length:
                total_bandwidth = output_len_tree.get_bandwidth_sum_total_less_than(Request.get_bandwidth_from_output_length(mid))
                if total_bandwidth <= tau_min and total_bandwidth > best_solution_bandwidth:
                    output_set = output_len_tree.get_all_less_than(mid)
                    best_solution_bandwidth = total_bandwidth
                    best_solution = output_set
                    best_solution_tau_min = tau_min
    
    # print(best_solution_tau_min, best_solution_bandwidth)
    return best_solution


# print(paper_1_sol(requests))
# print(opt_sol(requests))