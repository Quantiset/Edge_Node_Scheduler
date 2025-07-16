from utils import *
from avl import AVLTree
import random
import matplotlib.pyplot as plt

def plot_current(reqs: list[Request]):

    sizes = [a.get_bandwidth() for a in reqs]
    paper_2_times = [a.latency for a in reqs]
    epochs = [a.epoch for a in reqs]  

    print(epochs)

    fig = plt.figure(figsize=(12, 6))

    scatter = plt.scatter(
        sizes,
        paper_2_times,
        c=epochs,
        cmap='viridis',
        s=50,
        edgecolor='k'
    )

    plt.colorbar(scatter, label='Depth')
    plt.title("Prompt Scheduling split into epochs")
    plt.xlabel("f(s, n)")
    plt.ylabel("t")
    plt.grid(True)
    plt.show()


def opt_sol(requs: list[Request], plot = False):

    dropped_requests, dropped_set = handle_impossible_requests(requs)
    reqs = [r for r in requs if r not in dropped_set]

    ret = []
    last_reqs = len(reqs) + 1
    i = 0

    while reqs:
        i += 1

        print(f"Remaining requests: {len(reqs)}", last_reqs - len(reqs))
        if last_reqs - len(reqs) == 0:
            print("No more requests can be removed, breaking out of the loop.")
            for request in reqs:
                request.epoch = i+1
                ret.append(request)
            break
        last_reqs = len(reqs)

        best_solution = []
        best_solution_bandwidth = 0

        highest_f = 0
        tree = AVLTree()
        reqs.sort(key=lambda x: x.latency, reverse=True)

        smallest_output = float('inf')
        for request in reqs: # up-down pass,
            tau_min = request.latency
            highest_f = max(highest_f, request.get_bandwidth())
            tree.insert(request)

            lo, hi = 0, highest_f + 1
            while lo < hi:
                mid = (lo + hi) // 2
                if tree.get_bandwidth_sum_total_less_than(mid) < tau_min:
                    lo = mid + 1
                else:
                    hi = mid

            total_bandwidth = tree.get_bandwidth_sum_total_less_than(mid-1)
            output_set = tree.get_all_less_than(mid)
            if total_bandwidth <= tau_min and len(output_set) > len(best_solution):
                best_solution_bandwidth = total_bandwidth
                best_solution = output_set
                # print(best_solution)

        for request in best_solution:
            request.epoch = i
            ret.append(request)
        best_solution_set = set(best_solution)
        reqs = [r for r in reqs if r not in best_solution_set]
    
    for elem in dropped_set:
        elem.epoch = ret[-1].epoch+1 if ret else 0
        ret.append(elem)

    if plot:
        plot_current(ret)

    return ret


if __name__ == "__main__":
    random.seed(87)  # For reproducibility

    size = 600
    requests = [
        Request(i, random.randint(1, 150), random.randint(1, 150), random.randint(20000, 90000), random.randint(1, 150))
        for i in range(size)
    ]
    opt_sol(requests, True)
