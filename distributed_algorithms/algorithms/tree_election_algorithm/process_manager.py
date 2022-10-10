from random import randint, choice, shuffle
from typing import List
from treelib import Tree
from .tree_election_process import TreeElectionProcess
from ...generic.messages import MessageManager


def generate_processes(num_processes: int, display_tree=False) -> (List[TreeElectionProcess], MessageManager):
    """Generates the processes with message manager and randomly orders them in a tree"""
    assert num_processes >= 2

    # Message manager for processes
    msg_manager = MessageManager(delay_msg=True)

    # Tree with random root
    process_num = list(range(1, 1000))
    process_i = randint(0, len(process_num) - 1)
    root = TreeElectionProcess(process_num[process_i], msg_manager)
    del process_num[process_i]
    processes = [root]

    # Tree used for display
    tree = Tree()
    tree.create_node(str(processes[0]), str(processes[0]))

    # Create processes and add to tree
    for i in range(0, num_processes - 1):
        # Create random node
        process_i = randint(0, len(process_num) - 1)
        process = TreeElectionProcess(process_num[process_i], msg_manager)
        del process_num[process_i]

        # Pick random parent and add child
        rand_parent = choice(processes)
        rand_parent.add_neigh(process.p_id)
        process.add_neigh(rand_parent.p_id)

        # Add process to tree display
        tree.create_node(str(process), str(process), parent=str(rand_parent))

        # Add process to processes
        processes.append(process)

    if display_tree:
        # Display tree generated
        print("Tree generated: ")
        tree.show()

    # Randomly reorder processes in list
    shuffle(processes)

    return processes, msg_manager


def run_tree_election_algorithm(num_processes: int):
    """Runs the tree election algorithm and displays the tree and logs from processes"""
    # Generate processes
    processes, msg_manager = generate_processes(num_processes, display_tree=True)

    # Initialise message manager and processes
    msg_manager.initialise(processes)
    rand_initiator = choice(processes)
    for process in processes:
        if process == rand_initiator:
            process.initialise(initiator=True)
        else:
            process.initialise()

    while len([process for process in processes if not process.decide]) > 0:
        # Wait until the processes have all decided
        pass

    # Output logs
    print("Logs from processes:")
    print("\n".join(msg_manager.logs))
    print()

    # Message count
    print(f"Total number of messages sent during tree election algorithm: {msg_manager.message_count}\n")
