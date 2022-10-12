from typing import List
import networkx as nx
from matplotlib import pyplot as plt

from distributed_algorithms.generic.process import GenericProcess


def display_graph(graph: nx.Graph, title: str):
    """Draws the graph in a window"""
    nx.draw_networkx(graph)
    plt.title(title)
    plt.show()


def count_edges(processes: List[GenericProcess]) -> int:
    return sum(len(p.neigh) for p in processes) // 2
