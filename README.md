# Overview

The package helps find an optimal rooted tree in an undirected vertex-weighted graph, which maximizes the total prize given a budget constraint. The algorithm is loosely inspired by the 2018 publication by Bateni MH, Hajiaghayi MT, Liaghat V (doi: 10.1137/15M102695X). The code first finds the "shortest" vertex-weighted rooted tree and then trims its zero-prize and lowest value leaves until its total cost fits the budget.

# Sample graph

In order to use the package, one needs to have an adjacency matrix as a 2D `numpy.ndarray` as well as two vectors of weights and prizes (again as 1D `numpy.ndarray`) for the vertices. The root should be the very first vertex (with the index zero). Below there is a code that creates a random graph with 500 vertices, 750 edges, and 300 prizes. It can be used to test how this package works.

```python
adj_matrix = np.zeros(shape=(500, 500), dtype=int)
adj = np.random.choice(a=range(499*250), size=750, replace=False)

def indexize(x, column):
    while 499 - column > 0:
        if x >= 499 - column:
            x -= 499 - column
            column += 1
        else:
            return 1 + column + x, column
    raise ValueError()
    
indexize = np.vectorize(indexize)

adj = indexize(adj, np.zeros(750, dtype=int))

for row, col in np.array(adj).T:
    adj_matrix[row, col] = adj_matrix[col, row] = 1
    
weights = np.random.randint(1, 40, size=500)
prizes = np.random.randint(10, 400, size=500)
prizes[0] = 0
zero_prizes = np.random.choice(a=range(499), size=199, replace=False) + 1
zero_prizes.sort()
prizes[zero_prizes] = 0

weights[0] = prize_to_cost[0] = 0
```

# Installation

The package can be installed as usual in Python: with `pip install nodeweightedbudget` command.

# How to use

The package has only one class that is expected to be used: `nodeweightedbudget.Graph(prizes, weights, budget)`. The expected workflow is the following:

```python
import nodeweightedbudget as nwb
import pandas as pd

graph = nwb.Graph(prizes=prizes, weights=weights, budget=3000)
graph.find_short_path(adj_matrix=adj_matrix, depth=0, previous=None, current=0)
graph = graph.trim()
while graph.total_weight > graph.budget:
    graph = graph.trim_one_leaf()
    
pd.DataFrame(graph.get_adj_matrix()).to_csv("result.csv", header=None, index=None)
```
