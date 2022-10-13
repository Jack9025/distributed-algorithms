from random import randint, choice, shuffle
from typing import List
from treelib import Tree
from .echo_process import EchoProcess
import networkx as nx
from ...generic.graph import display_graph, count_edges
from ...generic.messages import MessageManager


def generate_processes(num_processes: int, display=False) -> (List[EchoProcess], MessageManager):
    """Generates the processes with message manager and randomly links them together"""
    assert num_processes >= 2

    # Message manager
    msg_manager = MessageManager(delay_msg=True)

    # Graph
    g = nx.Graph()

    # Create a tree
    processes = [EchoProcess(1, msg_manager)]
    nodes = [EchoProcess(x, msg_manager) for x in range(2, num_processes + 1)]

    while len(nodes) > 0:
        # Pick random node
        i = randint(0, len(nodes) - 1)
        current_node = nodes[i]

        # Pick random parent
        parent = choice(processes)
        parent.add_neigh(current_node.p_id)
        current_node.add_neigh(parent.p_id)

        # Add edge to graph
        g.add_edge(current_node.p_id, parent.p_id)

        # Add process to processes
        processes += [current_node]

        # Remove from nodes to add
        del nodes[i]

    shuffle(processes)

    # Add additional random edges
    for process in processes:
        available = [q for q in processes if q != process and q.p_id not in process.neigh]
        shuffle(available)
        for i in range(randint(0, 3 if len(available) > 3 else len(available))):
            # Add neighbour to processes
            process.add_neigh(available[i].p_id)
            available[i].add_neigh(process.p_id)

            # Add edge to graph
            g.add_edge(process.p_id, available[i].p_id)

    shuffle(processes)

    if display:
        # Display the generated graph
        display_graph(g, "Network before echo algorithm")

    return processes, msg_manager


def find_tree(processes: List[EchoProcess], initiator: EchoProcess, display=False, execution_num: int = None) -> Tree:
    """Finds the tree from processes after the echo algorithm has been executed"""
    process_dict = {p.p_id: p for p in processes}  # Index process with its id
    g = nx.Graph()  # Graph for matplot
    tree = Tree()  # Tree for console

    # Create the tree using breath first search
    visited = []
    queue = [initiator]
    while len(queue) > 0:
        node = queue[0]
        del queue[0]
        if node.father:
            if node.father not in visited:
                continue  # Wait until father is added
            tree.create_node(str(node), str(node), parent=str(process_dict[node.father]))
            g.add_edge(node.p_id, node.father)
        else:
            tree.create_node(str(node), str(node))
        for n in node.neigh:
            if n not in visited and process_dict[n] not in queue:
                queue.append(process_dict[n])
        visited.append(node.p_id)

    if display:
        # Display the tree
        title = "Tree generated by echo algorithm"
        if execution_num:
            title = f"{title} (#{execution_num})"
        display_graph(g, title)

    return tree


def execute_echo_algorithm(processes: List[EchoProcess], msg_manager: MessageManager,
                           display_logs: bool = True, execution_num: int = None):
    # Initialise message manager and processes
    msg_manager.reset()
    msg_manager.initialise(processes)
    initiator = None
    for process in processes:
        process.reset()
        if not initiator:
            # Create initiator
            process.initialise(initiator=True)
            initiator = process
        else:
            # Initialise non-initiator
            process.initialise()

    while not initiator.decide:
        # Wait until initiator has decided
        pass

    if display_logs:
        # Display logs
        print("Logs from processes:")
        print('\n'.join(msg_manager.logs))
        print()

    # Display tree generated by echo algorithm
    print("Tree produced by echo algorithm from processes:")
    tree = find_tree(processes, initiator, display=True, execution_num=execution_num)
    tree.show()

    # Message count
    print(f"Total number of messages sent during echo algorithm: {msg_manager.message_count}\n")


def run_echo_algorithm(num_processes: int, display_logs: bool = True, num_executions: int = 1):
    # Generate processes with message manager
    processes, msg_manager = generate_processes(num_processes, display=True)
    print("Generated processes:")
    print(f"- {len(processes)} processes")
    print(f"- {count_edges(processes)} edges\n")

    for i in range(num_executions):
        print(f"Running echo algorithm ({i + 1} / {num_executions}) ...\n")
        execute_echo_algorithm(processes=processes,
                               msg_manager=msg_manager,
                               display_logs=display_logs,
                               execution_num=i + 1 if num_executions > 1 else None)
