import random
import time
import matplotlib.pyplot as plt
from utils import *
from avl import AVLTree
from algo1_ontime import paper_1_sol
from algo2 import paper_2_sol
from fast_scheduler_ontime import opt_sol
from fast_scheduler_ontime_priority import opt_sol_with_priority
from static_ontime import static_sol



with open('example_requests.txt', 'r') as f:
    tmp_requests = [{field.split(": ")[0]: field.split(": ")[1] for field in line.removeprefix("[").removesuffix("]\n").split(", ")} for line in f.readlines()]
    requests = [Request(int(req['id']), int(float(req['inp'])), int(float(req['out'])), 8*int(float(req['latency'])), int(req['acc'])) for req in tmp_requests]


    # paper_1_sol(requests, True)
    opt_sol(requests, True)