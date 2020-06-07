import os
import sys


def extract_label_file(args):
    label_file = []
    if not args:
        label_file.append(['(stdin)', sys.stdin])
    else:
        for arg in args:
            if ':' in arg:
                label_file.append(arg.split(':'))
            else:
                label = os.path.splitext(arg)[0]  # extract filename as label
                label_file.append([label, arg])
    return label_file


def parse_event(line):
    if line.startswith('dnnl_verbose'):
        m = line.split(',')
        if len(m) == 11:
            return {
                'raw': line,
                'action': m[1],
                'eng': m[2],
                'name': m[3],
                'impl': m[4],
                'prop': m[5],
                'format': m[6],
                'aux': (m[7] + ' ' + m[8]).strip(),
                'problem': m[9],
                'time': float(m[10])
            }

    if line.startswith('mkldnn_verbose'):
        m = line.split(',')
        if len(m) == 9:
            return {
                'raw': line,
                'action': m[1],
                'eng': 'cpu',
                'name': m[2],
                'impl': m[3],
                'prop': m[4],
                'format': m[5],
                'aux': m[6],
                'problem': m[7],
                'time': float(m[8])
            }


def parse_file(file, delimiter=''):
    if file is sys.stdin:
        lines = [l.rstrip() for l in file]
    else:
        with open(os.path.expanduser(file)) as f:
            lines = f.read().split('\n')
    if delimiter and delimiter in lines:
        lines = lines[lines.index(delimiter) + 1:]
    return [l for l in (parse_event(line) for line in lines) if l is not None]
