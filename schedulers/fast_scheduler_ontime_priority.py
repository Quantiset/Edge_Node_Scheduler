from utils import *
from avl import AVLTree
import random
import matplotlib.pyplot as plt
from fast_scheduler_ontime import opt_sol

TEST_EPOCHS = 20

def visualize_priority_replacement(keep, removed, injected, epoch):

    plt.figure(figsize=(10, 6))
    
    # Keep set: standard selected requests after pruning
    plt.scatter(
        [r.get_bandwidth() for r in keep],
        [r.latency for r in keep],
        color='green',
        edgecolor='k',
        label='Standard scheduled (kept)',
        s=50,
        alpha=0.8
    )

    # Removed requests
    plt.scatter(
        [r.get_bandwidth() for r in removed],
        [r.latency for r in removed],
        color='red',
        edgecolor='k',
        label='Removed',
        marker='x',
        s=70
    )

    # Injected high-priority requests
    plt.scatter(
        [r.get_bandwidth() for r in injected],
        [r.latency for r in injected],
        color='blue',
        edgecolor='k',
        label='Injected (high-priority)',
        marker='^',
        s=60
    )

    plt.title(f"Epoch {epoch}: Priority Injection Visualization")
    plt.xlabel("f(s_i, n_i) = n + n²")
    plt.ylabel("τ (latency)")
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()


def plot_current(reqs):

    sizes = [a.get_bandwidth() for a in reqs]
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

def opt_sol_with_priority(reqs: list[Request], log=False, alpha=0.2):
    ret = []
    last_reqs = len(reqs) + 1
    i = 0

    # Step 0: Partition into high and low priority at start
    random.shuffle(reqs)
    cutoff = int(alpha * len(reqs))
    high_priority = reqs[:cutoff]
    low_priority = reqs[cutoff:]

    while low_priority:
        i += 1
        
        print(f"Remaining requests: {len(reqs)}", last_reqs - len(reqs))
        if last_reqs - len(low_priority) == 0:
            print("No more requests can be removed, breaking out of the loop.")
            for r in low_priority:
                r.epoch = i
                ret.append(r)
            break
        last_reqs = len(low_priority)

        best_solution = []
        best_bandwidth = 0
        highest_f = 0
        tree = AVLTree()
        low_priority.sort(key=lambda r: r.latency, reverse=True)

        for request in low_priority:
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

            total_bw = tree.get_bandwidth_sum_total_less_than(mid-1)
            output_set = tree.get_all_less_than(mid)
            if total_bw <= tau_min and len(output_set) > len(best_solution):
                best_solution = output_set
                best_bandwidth = total_bw
                best_tau_min = tau_min

        if not best_solution:
            break

        best_solution.sort(key=lambda r: r.output_length + r.output_length**2, reverse=True)
        k = int(alpha * len(best_solution))
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
            r.epoch = i
        ret.extend(current_epoch_set)

        # Remove scheduled requests
        ids_to_remove = set(r.id for r in current_epoch_set)
        low_priority = [r for r in low_priority if r.id not in ids_to_remove]
        high_priority = [r for r in high_priority if r.id not in ids_to_remove]
    
    if log:
        plot_current(ret)

    return ret


if __name__ == "__main__":
    random.seed(87)  # For reproducibility
    plot = []
    for i in range(1):
        size = 1600
        requests = [
            Request(i, random.randint(1, 150), random.randint(1, 150), random.randint(20000, 90000), random.randint(1, 150))
            for i in range(size)
        ]
        # requests = [
        #     Request(0, 0, 100, 90000, 1),
        # ]
        plot.extend(opt_sol_with_priority(requests))
    plot_current(plot)
