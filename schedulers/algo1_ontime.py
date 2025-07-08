from utils import *
from avl import AVLTree
import random
import matplotlib.pyplot as plt
from algo1 import is_valid

def plot_current(reqs):

    print(reqs)
    sizes = [a.output_length for a in reqs]
    paper_2_times = [a.latency for a in reqs]
    epochs = [a.epoch for a in reqs]  # Assume each `a` has a `depth` attribute

    fig = plt.figure(figsize=(12, 6))

    scatter = plt.scatter(
        sizes,
        paper_2_times,
        c=epochs,
        cmap='viridis',  # or 'plasma', 'inferno', 'coolwarm', etc.
        s=50,             # optional: size of points
        edgecolor='k'     # optional: black border for contrast
    )

    plt.colorbar(scatter, label='Depth')  # adds a color legend
    plt.title("Prompts Scheduling with number of epochs")
    plt.xlabel("Output Length")
    plt.ylabel("Latency")
    plt.grid(True)
    plt.show()


def opt_sol(reqs: list[Request]):

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

        reqs.sort(key=lambda x: x.latency, reverse=True)
        for z in range(len(reqs), 0, -1):
            for d in range(z, len(reqs) + 1):
                f_d = reqs[:d]
                f_d.sort(key=lambda x: x.output_length, reverse=True)
                s = f_d[:z]
                bandwidth = is_valid(s)
                if bandwidth and len(s) > len(best_solution):
                    best_solution = s

        for request in best_solution:
            request.epoch = i
            ret.append(request)
        best_solution_set = set(best_solution)
        reqs = [r for r in reqs if r not in best_solution_set]
        
    plot_current(ret)


if __name__ == "__main__":
    random.seed(87)  # For reproducibility
    size = 600
    requests = [
        Request(i, random.randint(1, 150), random.randint(1, 150), random.randint(20000, 90000), random.randint(1, 150))
        for i in range(size)
    ]
    opt_sol(requests)
