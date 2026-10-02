import concurrent.futures
from typing import Dict, List, Set, Tuple
import multiprocessing as mp


class ConcurrentGraphEngine:
    """
    Distributed-style Graph Engine leveraging multi-processing to calculate 
    graph-wide metrics (PageRank, Reachability) across partitioned subgraphs.
    """

    def __init__(self, num_workers: int = None) -> None:
        self.num_workers = num_workers or mp.cpu_count()
        self.adj_list: Dict[int, List[int]] = {}
        self.nodes: Set[int] = set()

    def add_edge(self, u: int, v: int) -> None:
        """Adds a directed edge from node u to node v."""
        if u not in self.adj_list:
            self.adj_list[u] = []
        self.adj_list[u].append(v)
        self.nodes.add(u)
        self.nodes.add(v)

    def _pagerank_worker(
        self, node_chunk: List[int], current_ranks: Dict[int, float], damping: float, N: int
    ) -> Dict[int, float]:
        """Worker task executing one iteration of PageRank over a node partition."""
        partial_ranks = {}
        for node in node_chunk:
            rank_sum = 0.0
            # Aggregate incoming rank contributions
            for source, neighbors in self.adj_list.items():
                if node in neighbors and len(neighbors) > 0:
                    rank_sum += current_ranks[source] / len(neighbors)
            
            partial_ranks[node] = ((1 - damping) / N) + (damping * rank_sum)
        return partial_ranks

    def compute_parallel_pagerank(
        self, damping: float = 0.85, max_iter: int = 20, tol: float = 1e-6
    ) -> Dict[int, float]:
        """
        Calculates PageRank vector concurrently by partitioning nodes 
        across multiple CPU process workers.
        """
        N = len(self.nodes)
        if N == 0:
            return {}

        node_list = list(self.nodes)
        ranks = {node: 1.0 / N for node in node_list}
        chunk_size = max(1, len(node_list) // self.num_workers)
        chunks = [node_list[i : i + chunk_size] for i in range(0, len(node_list), chunk_size)]

        for iteration in range(max_iter):
            new_ranks = {}
            with concurrent.futures.ProcessPoolExecutor(max_workers=self.num_workers) as executor:
                futures = [
                    executor.submit(self._pagerank_worker, chunk, ranks, damping, N)
                    for chunk in chunks
                ]
                for future in concurrent.futures.as_completed(futures):
                    new_ranks.update(future.result())

            # Convergence Check
            err = sum(abs(new_ranks[n] - ranks[n]) for n in node_list)
            ranks = new_ranks
            if err < tol:
                break

        return ranks
