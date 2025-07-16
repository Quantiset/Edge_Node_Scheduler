import random, time, sys
from utils import Request
sys.setrecursionlimit(10**7)

# paper constants
k_4 = 1.0
k_5 = 1.0


def paper_2_sol(reqs: list[Request]):
    i = 0
    ret = []
    last_len = len(reqs) + 1
    while True:
        best_solution = oneiter(reqs)
        print(f"Epoch {i+1}, found {len(best_solution)} requests")
        if not best_solution:
            break
        ret.extend(best_solution)
        s_best_solution = set(best_solution)
        i += 1
        for r in best_solution:
            r.epoch = i
        reqs = [r for r in reqs if r not in s_best_solution]
    return ret

def oneiter(I):
    n = len(I)

    # 0) precompute each req's bandwidth to a list
    latencies  = [r.latency for r in I]
    bandwidths = [r.get_bandwidth() for r in I]

    # 2–3) for z = n..1
    for z in range(n, 0, -1):
        # sort indices by descending latency
        idx_by_lat = sorted(range(n), key=lambda i: latencies[i], reverse=True)

        # 4) for d = z..n
        for d in range(z, n+1):
            # τ_min is the d-th largest latency
            tau_min = latencies[idx_by_lat[d-1]]

            # take top-d candidate *indices*
            cand = idx_by_lat[:d]
            bw_cand = [bandwidths[i] for i in cand]

            # --- EARLY PRUNE: if even the z smallest‐bw among these d exceed τ_min, skip
            smallest_z_bw = sorted(bw_cand)[:z]
            if sum(smallest_z_bw) > tau_min:
                continue

            # ALSO precompute prefix‐sum of these sorted bw to speed lower‐bound checks
            asc_bw = sorted(bw_cand)
            prefix_bw = [0.0]*(d+1)
            for i, bw in enumerate(asc_bw, start=1):
                prefix_bw[i] = prefix_bw[i-1] + bw

            # 6–9) DFS for this (z,d):
            stack = [
                # stack entries are tuples (next_pick_max_idx, chosen_list, current_bw)
                (d, [], 0.0)
            ]
            while stack:
                rem, chosen, cur_bw = stack.pop()
                picked = len(chosen)

                # #13 check full size
                if picked == z:
                    # valid because we only pushed nodes with cur_bw <= tau_min
                    return [ I[i] for i in chosen ]

                # #26 prune if not enough left
                if picked + rem < z:
                    continue

                min_extra_bw = prefix_bw[z-picked]  # sum of smallest (z-picked)
                if cur_bw + min_extra_bw > tau_min:
                    continue

                # generate children in descending index order
                for j in range(rem-1, -1, -1):
                    idx = cand[j]
                    nbw = cur_bw + bandwidths[idx]
                    if nbw > tau_min:
                        continue
                    # push state where we've taken candidate j, 
                    # so next rem becomes j
                    stack.append((j, chosen + [idx], nbw))

    return []


if __name__ == "__main__":
    # Example usage
    random.seed(87)  # For reproducibility 
    size = 50
    requests = [
        Request(i, random.randint(1, 150), random.randint(1, 150), random.randint(20000, 90000), random.randint(1, 150))
        for i in range(size)
    ]
    solution = solution2(requests)