import random
import time
import matplotlib.pyplot as plt
from utils import *
from avl import AVLTree
from unlim_bandwith import paper_1_sol, opt_sol

if __name__ == "__main__":
    random.seed(87)  # For reproducibility
    
    # call paper_1_sol and opt_sol with increasing larger inputs
    # structure each request as : for i in range(600): requests.append(Request(i, random.randint(1, 100), random.randint(1, 100), random.randint(30000, 60000), random.randint(1, 100)))
    # for instance, plot paper_1_sol and opt_sol with 100, 200, ..., 600 requests and graph the time taken by each

    sizes = list(range(50, 901, 50))
    paper_1_times = []
    opt_times = []
    for size in sizes:
        requests = [Request(i, random.randint(1, 100), random.randint(1, 100), random.randint(30000, 60000), random.randint(1, 100)) for i in range(size)]
        
        start_time = time.time()
        paper_1_sol(requests)
        paper_1_times.append(time.time() - start_time)
        
        start_time = time.time()
        opt_sol(requests)
        opt_times.append(time.time() - start_time)

        print(size)

    # Plotting the results
    plt.figure(figsize=(12, 6))
    plt.plot(sizes, paper_1_times, label='Paper 1 Solution Time', marker='o')
    plt.plot(sizes, opt_times, label='Optimal Solution Time', marker='o')
    plt.title('Time Complexity of Scheduling Solutions')
    plt.xlabel('Number of Requests')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.savefig('scheduling_time_complexity.png')
    plt.show()