from utils import Request

requests = [
    Request(1, 6, 10, 5, 2),
    Request(2, 9, 8, 3, 1),
    Request(3, 2, 12, 6, 3),
    Request(4, 5, 7, 2, 1),
]

requests.sort(key=lambda x: x.latency, reverse=True)
for z in range(len(requests), 0, -1):
    for d in range(z, len(requests) + 1):
        f_d.sort(key=lambda x: x.output_length, reverse=True)
        s = f_d[:z]
        s.append(f_d[d])
        if is_valid(s):
            print("valid", s)

