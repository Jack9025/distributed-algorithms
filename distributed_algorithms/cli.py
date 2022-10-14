import argparse
from distributed_algorithms.algorithms.echo_algorithm.process_manager import run_echo_algorithm
from distributed_algorithms.algorithms.echo_election_algorithm.process_manager import run_echo_election_algorithm
from distributed_algorithms.algorithms.tree_algorithm.process_manager import run_tree_algorithm
from distributed_algorithms.algorithms.tree_election_algorithm.process_manager import run_tree_election_algorithm


def tree_algorithm(args):
    run_tree_algorithm(args.processes)


def echo_algorithm(args):
    run_echo_algorithm(args.processes, args.hide_logs, args.executions)


def tree_election_algorithm(args):
    run_tree_election_algorithm(args.processes)


def echo_election_algorithm(args):
    run_echo_election_algorithm(args.processes, args.initiators, args.hide_logs, args.executions)


def cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Tree wave algorithm
    parser_tree = subparsers.add_parser('tree', help='runs the tree wave algorithm')
    parser_tree.set_defaults(func=tree_algorithm)
    parser_tree.add_argument('-n', '--processes', help='number of processes',
                             type=int, default=8, choices=range(2, 65))

    # Echo wave algorithm
    parser_echo = subparsers.add_parser('echo', help='runs the echo wave algorithm')
    parser_echo.set_defaults(func=echo_algorithm)
    parser_echo.add_argument('-n', '--processes', help='number of processes',
                             type=int, default=8, choices=range(2, 65))
    parser_echo.add_argument('-e', '--executions', help='number of executions',
                             type=int, default=1, choices=range(1, 10))
    parser_echo.add_argument('--hide-logs', action='store_const',
                             default=True, const=False, help="hides the logs produced by processes")

    # Tree election algorithm
    parser_tree_election = subparsers.add_parser('tree_election', help='runs the tree election algorithm')
    parser_tree_election.set_defaults(func=tree_election_algorithm)
    parser_tree_election.add_argument('-n', '--processes', help='number of processes',
                                      type=int, default=8, choices=range(2, 65))

    # Echo election algorithm
    parser_echo_election = subparsers.add_parser('echo_election', help='runs the echo election algorithm')
    parser_echo_election.set_defaults(func=echo_election_algorithm)
    parser_echo_election.add_argument('-n', '--processes', help='number of processes',
                                      type=int, default=8, choices=range(2, 65))
    parser_echo_election.add_argument('-i', '--initiators', help='number of initiators',
                                      type=int, default=1, choices=range(1, 65))
    parser_echo_election.add_argument('-e', '--executions', help='number of executions',
                                      type=int, default=1, choices=range(1, 10))
    parser_echo_election.add_argument('--hide-logs', action='store_const',
                                      default=True, const=False, help="hides the logs produced by processes")

    # Parse command line
    args = parser.parse_args()

    # Run algorithm
    try:
        args.func(args)
    except AttributeError:
        print("You need to select an algorithm to run. Type --help for more info.")
