import random
import time
import matplotlib.pyplot as plt
from utils import *
from avl import AVLTree
from schedulers.algo1 import paper_1_sol
from schedulers.algo2 import paper_2_sol
from schedulers.fast_scheduler import opt_sol


random.seed(87)  # For reproducibility

def graph_time_compare():
    
    # call paper_1_sol and opt_sol with increasing larger inputs
    # structure each request as : for i in range(600): requests.append(Request(i, random.randint(1, 100), random.randint(1, 100), random.randint(30000, 60000), random.randint(1, 100)))
    # for instance, plot paper_1_sol and opt_sol with 100, 200, ..., 600 requests and graph the time taken by each

    sizes = list(range(50, 3901, 50))
    paper_1_times = []
    paper_2_times = []
    opt_times = []
    for size in sizes:
        requests = [Request(i, random.randint(1, 100), random.randint(1, 100), random.randint(30000, 60000), random.randint(1, 100)) for i in range(size)]
        
        start_time = time.time()
        paper_1_sol(requests)
        paper_1_times.append(time.time() - start_time)
        
        start_time = time.time()
        paper_2_sol(requests)
        paper_1_times.append(time.time() - start_time)

        start_time = time.time()
        opt_sol(requests)
        opt_times.append(time.time() - start_time)

        print(size)

    # Plotting the results
    plt.figure(figsize=(12, 6))
    plt.plot(sizes, paper_1_times, label='Paper 1 Solution Time', marker='o')
    plt.plot(sizes, paper_2_times, label='Paper 2 Solution Time', marker='o')
    plt.plot(sizes, opt_times, label='Optimal Solution Time', marker='o')
    plt.title('Time Complexity of Scheduling Solutions')
    plt.xlabel('Number of Requests')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.savefig('../images/multiple_algos.png')
    plt.show()

if __name__ == "__main__":
    graph_time_compare()