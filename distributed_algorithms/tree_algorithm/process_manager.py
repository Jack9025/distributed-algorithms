from .message_manager import MessageManager
from random import randint, choice, shuffle
from .process import Process
from treelib import Tree

msg_manager = MessageManager()
logs = []


def log(msg):
    logs.append(msg)


def generate_processes(num_processes: int, display_tree=False) -> list:
    """Generates the processes and randomly orders them in a tree"""
    assert num_processes >= 2

    # Tree with root node 1
    root = Process(1, msg_manager)
    processes = [root]

    # Tree used for display
    tree = Tree()
    tree.create_node(str(root), str(root))

    # Node processes to add to tree
    nodes = [Process(x, msg_manager) for x in range(2, num_processes+1)]
    while len(nodes) > 0:
        # Pick random node
        i = randint(0, len(nodes) - 1)
        current_node = nodes[i]

        # Pick random parent and add child
        rand_parent = choice(processes)
        rand_parent.add_child(current_node)
        current_node.set_parent(rand_parent)

        # Add process to tree display
        tree.create_node(str(current_node), str(current_node), parent=str(rand_parent))

        # Add process to processes
        processes += [current_node]

        # Remove from nodes to add
        del nodes[i]

    if display_tree:
        # Display tree generated
        print("Tree generated: ")
        tree.show()

    # Randomly reorder processes in list
    shuffle(processes)

    return processes


def run_tree_algorithm(num_processes: int):
    """Runs the tree algorithm and displays the tree and logs from processes"""
    # Generate processes
    processes = generate_processes(num_processes, display_tree=True)

    # Initialise message manager and processes
    msg_manager.initialise(processes)
    for process in processes:
        process.initialise()

    while len([process for process in processes if not process.decide]) > 0:
        # Wait until the processes have all decided
        pass

    # Output logs
    print("Logs from processes:")
    print("\n".join(logs))
