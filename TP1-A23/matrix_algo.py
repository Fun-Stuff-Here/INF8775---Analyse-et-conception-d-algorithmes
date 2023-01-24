import argparse
import numpy as np
from time import perf_counter
import algo_tp1 as algo

SECOND_TO_MS = 1000

if __name__ == '__main__':
    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", dest="a", type=str, help="a: algorithm to use {conv, strassen, strassenSeuil}")
    parser.add_argument("-e1", dest="e1", type=str, help="e1: Path to first matrix exemple")
    parser.add_argument("-e2", dest="e2", type=str, help="e2: Path to second matrix exemple")
    parser.add_argument("-p", dest="p", type=bool, help="p: print the matrix", default=False, nargs='?')
    parser.add_argument("-t", dest="t", type=bool, help="t: print the time", default=False, nargs='?')
    args = parser.parse_args()

    if args.p is None:
        args.p = True
    if args.t is None:
        args.t = True

    with open(args.e1, 'r') as f:
        size1 = int(f.readline())
        array1 = np.loadtxt(f, dtype=int)
    with open(args.e2, 'r') as f:
        size2 = int(f.readline())
        array2 = np.loadtxt(f, dtype=int)
    

    start_time = perf_counter()
    if args.a == "conv":
        result = algo.conv(array1, array2, size1)
    elif args.a == "strassen":
        result = algo.strassen(array1, array2, size1)
    elif args.a == "strassenSeuil":
        result = algo.strassenSeuil(array1, array2, size1)
    end_time = perf_counter()

    if args.p:
        to_print_string = ""
        for i in range(size1):
            for j in range(size2):
                to_print_string += str(result[i][j]) + " "
            to_print_string += "\n"
        print(to_print_string)

    if args.t:
        print(str(SECOND_TO_MS*(end_time - start_time)))