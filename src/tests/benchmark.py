import time
import random
from src.engine import ConcurrentGraphEngine


def run_benchmark():
    engine = ConcurrentGraphEngine()
    print("Generating synthetic graph with 1,000 nodes and 5,000 edges...")
    for _ in range(5000):
        u = random.randint(0, 1000)
        v = random.randint(0, 1000)
        if u != v:
            engine.add_edge(u, v)

    start = time.time()
    ranks = engine.compute_parallel_pagerank(max_iter=10)
    elapsed = time.time() - start

    print(f"Parallel PageRank completed in {elapsed:.4f} seconds.")
    print(f"Top Node Rank Sample: {list(ranks.items())[:3]}")


if __name__ == "__main__":
    run_benchmark()
