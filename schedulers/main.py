import random
import time
import matplotlib.pyplot as plt
from utils import *
from avl import AVLTree
from algo1_ontime import paper_1_sol
from algo2_t2 import paper_2_sol
from fast_scheduler_ontime import opt_sol
from static_ontime import static_sol


random.seed(87)  # For reproducibility

def graph_time_compare():
    
    # call paper_1_sol and opt_sol with increasing larger inputs
    # structure each request as : for i in range(600): requests.append(Request(i, random.randint(1, 100), random.randint(1, 100), random.randint(30000, 60000), random.randint(1, 100)))
    # for instance, plot paper_1_sol and opt_sol with 100, 200, ..., 600 requests and graph the time taken by each

    sizes = list(range(25, 53, 2))
    paper_1_times = []
    static_times = []
    opt_times = []
    for size in sizes:
        requests = [Request(i, random.randint(1, 100), random.randint(1, 100), random.randint(30000, 60000), random.randint(1, 100)) for i in range(size)]
        
        start_time = time.time()
        paper_1_sol(requests)
        paper_1_times.append(time.time() - start_time)
        
        start_time = time.time()
        paper_2_sol(requests)
        static_times.append(max(0.001, time.time() - start_time))

        start_time = time.time()
        opt_sol(requests)
        opt_times.append(time.time() - start_time)

        print(size)

    # Plotting the results
    plt.figure(figsize=(12, 6))
    plt.plot(sizes, paper_1_times, label='Algorithm 1', marker='x')
    # plt.plot(sizes, paper_2_times, label='Paper 2 Solution Time', marker='o')
    plt.plot(sizes, static_times, label='OT-GAH', marker='o')
    plt.plot(sizes, opt_times, label='Our Algorithm', marker='v')
    plt.title('Time Comparison of Scheduling Algorithms')
    plt.xlabel('Number of Requests')
    plt.yscale('log')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.savefig('../images/multiple_algos.png')
    plt.show()

if __name__ == "__main__":
    graph_time_compare()