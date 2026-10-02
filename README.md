![Python Package CI](https://github.com/tess2005/distributed-graph-engine/actions/workflows/python-tests.yml/badge.svg)
# distributed-graph-engine
High-performance parallel graph processing engine implementing distributed PageRank and shortest-path algorithms with dynamic worker load balancing
## System Architecture

```mermaid
graph TD
    A[Input Graph / Edge List] --> B[Master Process / Load Balancer]
    B --> C[Worker Process 1: Node Chunk A]
    B --> D[Worker Process 2: Node Chunk B]
    B --> E[Worker Process 3: Node Chunk C]
    C --> F[Shared Memory / Queue Convergence]
    D --> F
    E --> F
    F --> G[Rank Matrix Output & Error Calculation]
```
