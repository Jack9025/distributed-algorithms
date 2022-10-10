import argparse
from distributed_algorithms.algorithms.echo_algorithm.process_manager import run_echo_algorithm
from distributed_algorithms.algorithms.tree_algorithm.process_manager import run_tree_algorithm
from distributed_algorithms.algorithms.tree_election_algorithm.process_manager import run_tree_election_algorithm


def tree_algorithm(args):
    run_tree_algorithm(args.num_processes)


def echo_algorithm(args):
    run_echo_algorithm(args.num_processes)


def tree_election_algorithm(args):
    run_tree_election_algorithm(args.num_processes)


def cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Tree wave algorithm
    parser_tree = subparsers.add_parser('tree', help='runs the tree wave algorithm')
    parser_tree.set_defaults(func=tree_algorithm)
    parser_tree.add_argument('-n', '--num_processes', help='number of processes',
                             type=int, default=8, choices=range(2, 65))

    # Echo wave algorithm
    parser_echo = subparsers.add_parser('echo', help='runs the echo wave algorithm')
    parser_echo.set_defaults(func=echo_algorithm)
    parser_echo.add_argument('-n', '--num_processes', help='number of processes',
                             type=int, default=8, choices=range(2, 65))

    # Tree election algorithm
    parser_echo = subparsers.add_parser('tree_election', help='runs the tree election algorithm')
    parser_echo.set_defaults(func=tree_election_algorithm)
    parser_echo.add_argument('-n', '--num_processes', help='number of processes',
                             type=int, default=8, choices=range(2, 65))

    # Parse command line
    args = parser.parse_args()

    # Run algorithm
    try:
        args.func(args)
    except AttributeError:
        print("You need to select an algorithm to run. Type --help for more info.")

