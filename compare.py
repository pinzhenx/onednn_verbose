import re
import common
from utils.parser import parse_file


class style():
    RED = '\033[31m'
    GREEN = '\033[32m'
    RESET = '\033[0m'


def filter_by_op_and_prop_kind(data, name, prop_kind=''):
    return list(filter(lambda e: e['name'] == name and prop_kind in e['prop'], data))


def strip_time_field(str):
    return re.match('(^.+),[^,]+$', str)[1]


def compare_single_op(label_a, events_a, label_b, events_b, thresh=1.5, show='all'):
    len_a = len(events_a)
    len_b = len(events_b)
    if len_a != len_b or len_a == 0 or len_b == 0:
        print('Skipped')
        return

    better_set = set()
    worse_set = set()
    better_cnt = 0
    worse_cnt = 0
    almost_same = 0
    line_cnt = 0
    for i in range(len_a):
        event_a = events_a[i]
        event_b = events_b[i]
        ratio = round(event_a['time'] / event_b['time'], 2)
        if ratio >= thresh:
            worse_cnt += 1
            raw_a = event_a['raw']
            raw_b = event_b['raw']
            worse_set.add((strip_time_field(raw_a), strip_time_field(raw_b)))
            if show in ['worse', 'all']:
                line_cnt += 1
                print(f"{line_cnt}. {label_a} / {label_b} = {style.RED}{ratio}{style.RESET}")
                print(f"({label_a}) {raw_a}")
                print(f"({label_b}) {raw_b}")
                print()
        elif ratio <= 1 / thresh:
            better_cnt += 1
            raw_a = event_a['raw']
            raw_b = event_b['raw']
            better_set.add((strip_time_field(raw_a), strip_time_field(raw_b)))
            if show in ['better', 'all']:
                line_cnt += 1
                print(f"{line_cnt}. {label_a} / {label_b} = {style.GREEN}{ratio}{style.RESET}")
                print(f"({label_a}) {raw_a}")
                print(f"({label_b}) {raw_b}")
                print()
        else:
            almost_same += 1
            if show == 'all':
                line_cnt += 1
                raw_a = event_a['raw']
                raw_b = event_b['raw']
                print(f"{line_cnt}. {label_a} / {label_b} = {ratio}")
                print(f"({label_a}) {raw_a}")
                print(f"({label_b}) {raw_b}")
                print()

    print('\n\nMuch better:    ', better_cnt)
    for i, case in enumerate(list(better_set)):
        print(f'{i}.')
        print(f'({label_a}) {case[0]}')
        print(f'({label_b}) {case[1]}')
        print()
    print('\n\nMuch worse:     ', worse_cnt)
    for i, case in enumerate(list(worse_set)):
        print(f'{i}.')
        print(f'({label_a}) {case[0]}')
        print(f'({label_b}) {case[1]}')
        print()
    print('\n\nAlmost the same:', almost_same)


# python compare.py -f=dnnl:dnnl.log -f=mkldnn:mkldnn.log \
#   --thresh=1.5 --show=worse --op=convolution --prop-kind=forward_training
if __name__ == '__main__':
    parser = common.ArgParser()
    parser.add_argument('--op', '-o')
    parser.add_argument('--prop-kind', '-p', default='')
    parser.add_argument('--thresh', '-t', type=float, default=1.5)
    parser.add_argument('--show', '-s', choices=['all', 'better', 'worse'], action='store', default='all')
    args = parser.parse_args()

    label_a, file_a = args.file[0].split(':')
    label_b, file_b = args.file[1].split(':')
    events_a = parse_file(file_a, args.delimiter)
    events_b = parse_file(file_b, args.delimiter)

    compare_single_op(
        label_a, filter_by_op_and_prop_kind(events_a, args.op, args.prop_kind),
        label_b, filter_by_op_and_prop_kind(events_b, args.op, args.prop_kind),
        show=args.show,
        thresh=args.thresh)
