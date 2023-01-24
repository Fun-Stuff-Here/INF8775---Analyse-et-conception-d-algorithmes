#!/bin/bash

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -a|--algo)
      ALGO="$2"
      shift # past argument
      shift # past value
      ;;
    -e1|--exemple1)
      PATH_TO_EX_1="$2"
      shift # past argument
      shift # past value
      ;;
      -e2|--exemple2)
      PATH_TO_EX_2="$2"
      shift # past argument
      shift # past value
      ;;
    -p|--print)
    PRINT_FLAG='-p'
    shift # past argument
    ;;
    -t|--showtime)
    SHOW_TIME_FLAG='-t'
    shift # past argument
    ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
  esac
done

python3 matrix_algo.py -a $ALGO -e1 $PATH_TO_EX_1 -e2 $PATH_TO_EX_2 $PRINT_FLAG $SHOW_TIME_FLAG
