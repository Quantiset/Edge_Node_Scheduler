
# paper variables
k_4 = 1.0
k_5 = 1.0
k_6 = 1000.0
import time
import random

class Request:
    def __init__(self, id, prompt_length, output_length, latency, accuracy):
        self.id = id
        self.prompt_length = prompt_length + random.random()
        self.output_length = output_length + random.random()
        self.latency = latency
        self.accuracy = accuracy
        self.creation_time = time.time()
        self.high_priority = False
        self.time_taken = 0
    
    def get_bandwidth(self):
        return self.get_bandwidth_from_request(self)
    
    @staticmethod
    def get_bandwidth_from_request(req):
        return req.prompt_length * k_4 + req.output_length * req.output_length * k_5
    
    def get_time(self):
        return ((time.time() - self.creation_time) * int(1*self.high_priority + 1)) ** 2
    
    def __repr__(self):
        return f"[id: {self.id}, inp: {self.prompt_length}, out: {self.output_length}, latency: {self.latency}, acc: {self.accuracy}, bandwidth: {self.get_bandwidth()}]"
    
    def __hash__(self):
        return self.id

def handle_impossible_requests(requests, epoch=999999999):
    dropped_requests = 0
    dropped_set = set()
    for req in requests:
        if req.get_bandwidth() > req.latency:
            req.epoch = epoch
            dropped_requests += 1
            dropped_set.add(req)
    return dropped_requests, dropped_set
