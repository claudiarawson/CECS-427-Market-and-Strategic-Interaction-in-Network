import sys
import networkx as nx
from networkx.algorithms import bipartite
import os
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

def compute_payoffs(graph):
    payoffs_by_buyer = defaultdict(list)
    
    for seller, buyer, attributes in graph.edges(data=True):
        seller_price = graph.nodes[seller]['price']
        valuation = attributes['valuation']
        payoff = valuation - seller_price

        payoffs_by_buyer[buyer].append((seller, payoff))
    
    return dict(payoffs_by_buyer)

def select_highest_payoffs(round):
    best_offer = {}
    for buyer, match in round.items():
        best_seller, max_payoff = max(match, key=lambda x: x[1])
        best_offer[buyer] = (best_seller, max_payoff)
    return best_offer

def identify_constrained_sets(best_matches):
    seller_list = [seller for seller, _ in best_matches.values()]
    seller_counts = Counter(seller_list)

    constrained = {seller for seller, count in seller_counts.items() if count > 1}
    
    return constrained

def increase_price(graph, sellers_to_update):
    for seller in sellers_to_update:
        current_price = graph.nodes[seller]['price']
        graph.nodes[seller]['price'] = current_price + 1
    

def draw_market_graph(graph, highlighted_matches=None):
    sellers, buyers = bipartite.sets(graph)

    positions = {
        node: (1, idx) for idx, node in enumerate(sellers)
    }
    positions.update({
        node: (2, idx) for idx, node in enumerate(buyers)
    })

    plt.figure(figsize=(10, 8))

    node_colors = ['lightblue' if node in sellers else 'lightgreen' for node in graph.nodes]
    nx.draw(graph, pos=positions, with_labels=True, node_size=500, font_size=10, node_color=node_colors)

    if highlighted_matches:
        matching_edges = [(seller, buyer) for buyer, (seller, _) in highlighted_matches.items()]
        nx.draw_networkx_edges(graph, positions, edgelist=matching_edges, edge_color='red', width=2)

    plt.title("Market Graph")
    plt.show()



def main():
    arguments = sys.argv

    if len(arguments) < 2:
        print("Error: No input file specified.")
        return

    input_path = arguments[1]

    if not os.path.isfile(input_path):
        print(f"Error: File '{input_path}' not found.")
        return

    try:
        market_graph = nx.read_gml(input_path)
    except nx.NetworkXError:
        print("Error: Invalid file format or corrupted GML file.")
        return

    if "--plot" in arguments:
        draw_market_graph(market_graph)

    payoffs = compute_payoffs(market_graph)
    optimal_matches = select_highest_payoffs(payoffs)
    blocked_sellers = identify_constrained_sets(optimal_matches)

    while blocked_sellers:
        print(f"Adjusting prices for constrained sellers: {blocked_sellers}")
        increase_price(market_graph, blocked_sellers)

        payoffs = compute_payoffs(market_graph)
        optimal_matches = select_highest_payoffs(payoffs)
        blocked_sellers = identify_constrained_sets(optimal_matches)

        if "--interactive" in arguments:
            draw_market_graph(market_graph, optimal_matches)

    print("Market cleared.")
    print("Final best payoffs:", optimal_matches)
    for buyer, (seller, _) in optimal_matches.items():
        print(f"Buyer {buyer} should buy from Seller {seller}")

if __name__ == "__main__":
    main()