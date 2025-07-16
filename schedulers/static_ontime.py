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


def static_sol(reqs: list[Request]):

    e_i = 0
    tmp = []
    for i, req in enumerate(reqs):
        query = tmp + [req]
        if is_valid(query):
            reqs[i].epoch = e_i
            tmp.append(req)
        else:
            e_i += 1
            reqs[i].epoch = e_i
            tmp = [reqs[i]]

    # plot_current(reqs)


if __name__ == "__main__":
    random.seed(87)  # For reproducibility 
    size = 600
    requests = [
        Request(i, random.randint(1, 150), random.randint(1, 150), random.randint(20000, 90000), random.randint(1, 150))
        for i in range(size)
    ]
    static_sol(requests)
