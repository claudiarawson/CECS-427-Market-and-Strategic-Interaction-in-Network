# Market Clearing Algorithm (Bipartite Graph Matching)

This project simulates a market-clearing algorithm using a bipartite graph to match buyers and sellers based on their valuations and prices. The goal is to resolve conflicts (i.e., when multiple buyers want the same seller) by adjusting prices iteratively until the market clears.

---

## Features

- Computes buyer payoffs from seller offers.
- Selects optimal matches based on maximum payoff.
- Detects over-demanded sellers (chosen by more than one buyer).
- Increases prices of over-demanded sellers to resolve conflicts.
- Visualizes the bipartite market graph (with optional highlights).
- Supports interactive and plot modes via command-line options.

---

## How It Works

- Buyers and sellers are represented as nodes in a bipartite graph.
- Edges between them contain valuation data (how much a buyer values an offer).
- Sellers have initial prices as node attributes.
- The algorithm:
  1. Computes payoffs (valuation - price).
  2. Selects best offer for each buyer.
  3. Identifies constrained sellers.
  4. Increases prices of constrained sellers.
  5. Repeats until the market clears (no over-demanded sellers).

---

## File Format

This script expects a **GML** file as input (Graph Modelling Language), which must include:

- Buyer and seller nodes.
- `"price"` attribute on seller nodes.
- `"valuation"` attribute on edges (from seller to buyer).

Example node and edge in GML:

```gml
node [
  id 0
  label "Seller_A"
  price 5
]

edge [
  source 0
  target 2
  valuation 10
]
```
## Usage
```py
python market_strategy.py path/to/graph.gml
```
**Optional Flags**

- `--plot` : Show the initial graph.

- `--interactive` : Visualize each iteration of price adjustment.

**Example**
```py
python market_strategy.py market.gml --plot --interactive
```

## Dependencies
- `networkx`
- `matplotlib`

Install with:
```bash
pip install networkx matplotlib
```
