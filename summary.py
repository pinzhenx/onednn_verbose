import math
import common
import functools
from utils.parser import parse_file, extract_label_file


def summarize(events, label=''):
    dataset = {}
    for e in events:
        opname = e['name']
        if opname not in dataset:
            dataset[opname] = {}
        op_stat = dataset[opname]

        prop_kind = 'forward' if e['prop'] == 'undef' else e['prop']
        if prop_kind not in op_stat:
            op_stat[prop_kind] = {
                'num_calls': 1,
                'time': e['time']
            }
        else:
            event_stat = op_stat[prop_kind]
            event_stat['num_calls'] += 1
            event_stat['time'] += e['time']
    return {'label': label, 'dataset': dataset}


def find_max_time(dic):
    def _find_max_time(dic, max_time):
        for key, value in dic.items():
            if key == 'time':
                return max(value, max_time)
            if isinstance(value, dict):
                max_time = max(max_time, _find_max_time(value, max_time))
        return max_time
    return _find_max_time(dic, 0)


def build_barchart(ratio=0, maxlen=45, mark='░'):
    return mark * math.ceil(ratio * maxlen)


def display_table(summaries):
    max_time = functools.reduce(lambda x, y: max(x, find_max_time(y)), summaries, 0)

    print(f"{'-' * 3} {'-' * 8} {'-' * 7} {'-' * 12}  {'-' * 45}")
    print('%2s  %-8s %7s %12s' % ('Op', 'Name', '#Calls', 'Time (ms)'))
    print(f"{'-' * 3} {'-' * 8} {'-' * 7} {'-' * 12}  {'-' * 45}")

    op_pkind = {}
    for summary in summaries:
        for opname, pkinds in summary['dataset'].items():
            if opname not in op_pkind:
                op_pkind[opname] = set()
            op_pkind[opname] |= set(pkinds.keys())

    for op_name, pkind_set in sorted(op_pkind.items()):
        print(op_name)
        for prop_kind in sorted(pkind_set):
            print(f'  {prop_kind}')
            for summary in summaries:
                label = summary['label']
                dataset = summary['dataset']
                op = dataset.get(op_name, {}).get(prop_kind, {})
                t = op.get('time', 0)
                num_calls = op.get('num_calls', 0)
                bar = build_barchart(t / max_time)
                print('    %-8s %7d %12.3f  %s' % (label, num_calls, t, bar))
        print()


# 1. compare multiple summaries
#      python summary.py -f=dnnl:dnnl.log -f=mkldnn:mkldnn.log
# 2. get summary from stdin/pipe
#      MKLDNN_VERBOSE=1 python foo.py | python summary.py
if __name__ == '__main__':
    parser = common.ArgParser()
    args = parser.parse_args()

    s = [summarize(parse_file(file, args.delimiter), label)
         for label, file in extract_label_file(args.file)]
    display_table(s)
