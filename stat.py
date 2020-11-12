import common
from utils import tab, miniserver
from utils.parser import parse_file, extract_label_file
from utils.csv_util import CsvBuilder
from utils.math import mean, std


def compute_stat(series):
    return {
        'cnt': len(series),
        'avg': mean(series),
        'std': std(series),
        'min': min(series),
        'max': max(series),
    }


def get_stat(events_label_list):
    labels = []
    occur_order = []
    key_to_label_to_series = {}
    for events, label in events_label_list:
        labels.append(label)
        for e in events:
            key = (e['action'], e['eng'], e['name'], e['impl'], e['prop'], e['format'], e['aux'], e['problem'])
            if key not in key_to_label_to_series:
                key_to_label_to_series[key] = {}
                occur_order.append(key)
            label_to_series = key_to_label_to_series[key]
            if label not in label_to_series:
                label_to_series[label] = []
            label_to_series[label].append(e['time'])

    primitive_stats = []
    for key in occur_order:
        label_to_series = key_to_label_to_series[key]
        stats = {l: compute_stat(s) for l, s in label_to_series.items()}
        primitive_stats.append({'key': key, 'stats': stats})
    return {'labels': labels, 'primitives': primitive_stats}


def big_difference(a, b):
    thresh = 1.2
    return a / b > thresh or b / a > thresh


def _build_stats_row(stats, labels):
    row_data = []
    for label in labels:
        if label in stats:
            stat = stats[label]
            cnt = str(stat['cnt'])
            mmin = '%.2g' % stat['min']
            mmax = '%.2g' % stat['max']
            coeff = '%.1f%%' % (stat['std'] / stat['avg'] * 100)
            avg = '%.3g' % stat['avg']
            for other in labels:
                if other != label and other in stats and \
                        big_difference(stat['avg'], stats[other]['avg']):
                    avg = f'*{avg}*'  # highlight the cell content
                    break
            row_data += [cnt, avg, mmin, mmax, coeff]
        else:
            row_data += ['-', '-', '-', '-', '-']
    return row_data


def build_csv(merged_stats):
    primitives = merged_stats['primitives']
    labels = merged_stats['labels']
    csv = CsvBuilder()

    # build first row of header
    header = []
    for c in ['#', 'act', 'eng', 'name', 'impl', 'prop', 'format', 'aux', 'problem']:
        header.append(CsvBuilder.span_row(c, 1))  # span field to the next row
    for l in labels:
        header.append(CsvBuilder.span_col(l, 4))  # span field to next 4 cols
    csv.add_row(header)
    csv.add_row(['calls', 'avg', 'min', 'max', 'std/avg'] * len(labels))
    csv.add_header_end()

    for idx, primitive in enumerate(primitives, 1):
        row_data = [str(idx), *primitive['key']]
        row_data += _build_stats_row(primitive['stats'], labels)
        csv.add_row(row_data)

    return csv.dump()


if __name__ == '__main__':
    parser = common.ArgParser()
    args = parser.parse_args()

    s = get_stat([[parse_file(file, args.delimiter), label]
                  for label, file in extract_label_file(args.file)])
    csv = build_csv(s)
    html = tab.csv2html(csv)
    miniserver.serve_single_page(html)
