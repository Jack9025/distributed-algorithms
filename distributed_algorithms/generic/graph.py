from threading import Thread
import networkx as nx
from matplotlib import pyplot as plt


def display_graph(graph: nx.Graph, title: str):
    """Draws the graph in a window"""
    nx.draw_networkx(graph)
    plt.title(title)
    plt.show()
