import argparse


def ArgParser():
    parser = argparse.ArgumentParser(description='OneDNN Verbose Toolkit')
    parser.add_argument('--file', '-f', action='append', help='label:filepath')
    parser.add_argument('--delimiter', '-d', default='')
    return parser
