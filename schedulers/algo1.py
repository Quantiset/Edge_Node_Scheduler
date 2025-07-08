
from utils import *
from avl import AVLTree

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



# print(paper_1_sol(requests))
# print(opt_sol(requests))