import argparse
import numpy as np
from time import perf_counter
import implementation as algo

SECOND_TO_MS = 1000

if __name__ == '__main__':
    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", dest="a", type=str, help="a: algorithm to use {conv, strassen, strassenSeuil}")
    parser.add_argument("-e", dest="e", type=str, help="e: Path to the exemple")
    parser.add_argument("-p", dest="p", type=bool, help="p: print the matrix", default=False, nargs='?')
    parser.add_argument("-t", dest="t", type=bool, help="t: print the time", default=False, nargs='?')
    args = parser.parse_args()

    if args.p is None:
        args.p = True
    if args.t is None:
        args.t = True

    # TODO: read the file
    with open(args.e, 'r') as f:
        pass

    start_time = perf_counter()
    if args.a == "glouton":
        result = algo.glouton()
    elif args.a == "progdyn":
        result = algo.progdyn()
    elif args.a == "approx":
        result = algo.approx()
    end_time = perf_counter()

    # TODO: print the result
    if args.p:
        pass

    if args.t:
        print(str(SECOND_TO_MS*(end_time - start_time)))