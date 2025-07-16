import numpy as np
from utils import *
from avl import AVLTree
import random
import matplotlib.pyplot as plt
from fast_scheduler_ontime import opt_sol

TEST_EPOCHS = 10
INSERT_SIZE = 200

def plot_heatmap():
    alphas = np.linspace(0, 0.7, 16)  
    betas = np.linspace(0, 0.7, 16)

    # Create an empty matrix to hold "dropped" values
    dropped_matrix = np.zeros((len(betas), len(alphas)))

    # Populate the matrix
    for i, beta in enumerate(betas):
        for j, alpha in enumerate(alphas):
            _, dropped, time_taken = opt_sol_with_priority(alpha=alpha, beta=beta)
            dropped_matrix[i, j] = dropped

    # Plot the heatmap
    plt.figure(figsize=(8, 6))
    c = plt.imshow(dropped_matrix, origin='lower', cmap='viridis',
                extent=[alphas[0], alphas[-1], betas[0], betas[-1]],
                aspect='auto')
    plt.colorbar(c, label='Dropped Requests')

    # Axis labels and title
    plt.xlabel('Alpha (High Priority Fraction)')
    plt.ylabel('Beta')
    plt.title('Dropped Requests vs Alpha and Beta')

    # Add numeric labels on each cell (optional)
    for i in range(len(betas)):
        for j in range(len(alphas)):
            plt.text(alphas[j], betas[i], f"{int(dropped_matrix[i, j])}",
                    ha='center', va='center', color='white', fontsize=8)

    plt.tight_layout()
    plt.show()

def plot_current(reqs):

    sizes = [a.output_length + a.output_length*a.output_length for a in reqs]
    paper_2_times = [a.latency for a in reqs]
    epochs = [a.epoch for a in reqs]  

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

def opt_sol_with_priority(alpha=0.0, beta=0.2):
    ret = []
    total_time = 0.0

    dropped_requests = 0
    high_priority = []
    low_priority = []
    med_priority = [
        Request(i, random.randint(1, 150), random.randint(1, 150), random.randint(20000, 90000), random.randint(1, 150))
        for i in range(INSERT_SIZE//2)
    ]

    last_reqs = 0 + 1

    for i in range(TEST_EPOCHS):

        ii = 0
        while True:
            ii += 1
            
            # insert requests
            to_insert = [
                Request(i, random.randint(1, 150), random.randint(1, 150), random.randint(20000, 90000), random.randint(1, 150))
                for i in range(INSERT_SIZE)
            ]
            high_priority.extend(to_insert[:int(alpha * INSERT_SIZE)])
            for hp in high_priority:
                hp.high_priority = True
            low_priority.extend(to_insert[int(alpha * INSERT_SIZE):])
        
            print(f"Remaining requests: {len(med_priority)}", last_reqs - len(med_priority))
            if last_reqs - len(med_priority) == 0:
                # print("No more requests can be removed, breaking out of the loop.")
                break
            last_reqs = len(med_priority)

            best_solution = []
            best_bandwidth = 0
            highest_output = 0
            tree = AVLTree()
            med_priority.sort(key=lambda r: r.latency, reverse=True)

            for request in med_priority:
                tau_min = request.latency
                highest_output = max(highest_output, request.output_length)
                tree.insert(request)

                lo, hi = 0, highest_output + 1
                while lo < hi:
                    mid = (lo + hi) // 2
                    if tree.get_bandwidth_sum_total_less_than(Request.get_bandwidth_from_output_length(mid)) < tau_min:
                        lo = mid + 1
                    else:
                        hi = mid

                total_bw = tree.get_bandwidth_sum_total_less_than(Request.get_bandwidth_from_output_length(mid - 1))
                output_set = tree.get_all_less_than(mid)
                if total_bw <= tau_min and len(output_set) > len(best_solution):
                    best_solution = output_set
                    best_bandwidth = total_bw
                    best_tau_min = tau_min

            best_solution.sort(key=lambda r: r.output_length + r.output_length**2, reverse=True)
            k = int(beta * len(best_solution))
            to_remove = best_solution[:k]
            keep = best_solution[k:]
            budget = sum(Request.get_bandwidth_from_output_length(r.output_length) for r in to_remove)

            candidates = [r for r in high_priority if r.latency >= best_tau_min]
            candidates.sort(key=lambda r: r.output_length + r.output_length**2)

            replacement = []
            total_bw = 0
            for r in candidates:
                bw = Request.get_bandwidth_from_output_length(r.output_length)
                if total_bw + bw <= budget:
                    total_bw += bw
                    replacement.append(r)
                if total_bw >= budget:
                    break

            # Finalize current epoch
            current_epoch_set = keep + replacement
            # visualize_priority_replacement(keep, to_remove, replacement, i)
            for r in current_epoch_set:
                total_time += r.get_time()
                r.epoch = ii
            ret.extend(current_epoch_set)

            # Remove scheduled requests
            ids_to_remove = set(r.id for r in current_epoch_set)
            med_priority = [r for r in med_priority if r.id not in ids_to_remove]
            high_priority = [r for r in high_priority if r.id not in ids_to_remove]
        
        dropped_requests += len(med_priority)
        for r in med_priority:
            total_time += r.get_time()
            r.epoch = 99999999

        med_priority = low_priority + high_priority
        low_priority = []
        high_priority = []

    print(f"Dropped requests: {dropped_requests} \nTotal squared time: {total_time:.2f} seconds")
    return ret, dropped_requests, total_time

def rest():
    random.seed(87)  # For reproducibility
    plot = []
    requests, dropped, total_time = opt_sol_with_priority(alpha=0.0, beta=0.0)
    plot.extend(requests)
    plot_current(plot)


if __name__ == "__main__":
    plot_heatmap()
    # rest()
