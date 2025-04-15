from collections import defaultdict, Counter
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import sys
import os
import networkx as nx

# Calculate payoff for each buyer based on the difference between their valuation and seller price
def compute_payoffs(graph):
    payoffs_by_buyer = defaultdict(list)
    
    for seller, buyer, attributes in graph.edges(data=True):
        seller_price = graph.nodes[seller]['price']
        valuation = attributes['valuation']
        payoff = valuation - seller_price

        payoffs_by_buyer[buyer].append((seller, payoff))
    
    return dict(payoffs_by_buyer)

# For each buyer, select the seller offering the highest payoff
def select_highest_payoffs(round):
    best_offer = {}
    for buyer, match in round.items():
        best_seller, max_payoff = max(match, key=lambda x: x[1])
        best_offer[buyer] = (best_seller, max_payoff)
    return best_offer

# Identify sellers that are selected by more than one buyer (i.e., over-demanded)
def identify_constrained_sets(best_matches):
    seller_list = [seller for seller, _ in best_matches.values()]
    seller_counts = Counter(seller_list)

    constrained = {seller for seller, count in seller_counts.items() if count > 1}
    
    return constrained

# Increase the price of sellers who are over-demanded
def increase_price(graph, sellers_to_update):
    for seller in sellers_to_update:
        current_price = graph.nodes[seller]['price']
        graph.nodes[seller]['price'] = current_price + 1
    
# Visualize the bipartite market graph with optional highlighted matches
def draw_market_graph(graph, highlighted_matches=None):
    sellers, buyers = bipartite.sets(graph)

    # Set positions for sellers and buyers
    positions = {
        node: (1, idx) for idx, node in enumerate(sellers)
    }
    positions.update({
        node: (2, idx) for idx, node in enumerate(buyers)
    })

    plt.figure(figsize=(10, 8))

    # Color nodes based on group
    node_colors = ['lightblue' if node in sellers else 'lightgreen' for node in graph.nodes]
    nx.draw(graph, pos=positions, with_labels=True, node_size=500, font_size=10, node_color=node_colors)

    # Highlight optimal matches in red
    if highlighted_matches:
        matching_edges = [(seller, buyer) for buyer, (seller, _) in highlighted_matches.items()]
        nx.draw_networkx_edges(graph, positions, edgelist=matching_edges, edge_color='red', width=2)

    plt.title("Market Graph")
    plt.show()

# Entry point of the script
def main():
    arguments = sys.argv

    # Check if input file was provided
    if len(arguments) < 2:
        print("Error: No input file specified.")
        return

    input_path = arguments[1]

    # Check if file exists
    if not os.path.isfile(input_path):
        print(f"Error: File '{input_path}' not found.")
        return

    # Try to read the graph from a GML file
    try:
        market_graph = nx.read_gml(input_path)
    except nx.NetworkXError:
        print("Error: Invalid file format or corrupted GML file.")
        return

    if "--plot" in arguments:
        draw_market_graph(market_graph)

    # Start the market clearing process
    payoffs = compute_payoffs(market_graph)
    optimal_matches = select_highest_payoffs(payoffs)
    blocked_sellers = identify_constrained_sets(optimal_matches)

    # Iteratively adjust prices until no seller is over-demanded
    while blocked_sellers:
        print(f"Adjusting prices for constrained sellers: {blocked_sellers}")
        increase_price(market_graph, blocked_sellers)

        payoffs = compute_payoffs(market_graph)
        optimal_matches = select_highest_payoffs(payoffs)
        blocked_sellers = identify_constrained_sets(optimal_matches)

        if "--interactive" in arguments:
            draw_market_graph(market_graph, optimal_matches)

    # Print final results
    print("Market cleared.")
    print("Final best payoffs:", optimal_matches)
    for buyer, (seller, _) in optimal_matches.items():
        print(f"Buyer {buyer} should buy from Seller {seller}")

# Run the main function if script is executed
if __name__ == "__main__":
    main()