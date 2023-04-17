#!/bin/bash
POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -e|--exemple)
      PATH_TO_EX="$2"
      shift # past argument
      shift # past value
      ;;
    -p|--print)
    PRINT_FLAG='-p'
    shift # past argument
    ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
  esac
done


python3 parsing.py -e $PATH_TO_EX $PRINT_FLAG
