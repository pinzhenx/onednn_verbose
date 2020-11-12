import common
from utils.parser import parse_file, extract_label_file


def merge_csv(file_events, filename):
    header = 'file,action,engine,primitive,impl,pkind,format,aux,problem,time'
    lines = [header]
    for fname, events in file_events.items():
        for e in events:
            lines.append(
                f"\"{fname}\",\"{e['action']}\",\"{e['eng']}\",\"{e['name']}\",\"{e['impl']}\",\"{e['prop']}\",\"{e['format']}\",\"{e['aux']}\",\"{e['problem']}\",\"{e['time']}\"")

    with open(filename, 'w+') as f:
        f.write('\n'.join(lines))
        print('Written to', filename)


if __name__ == '__main__':
    parser = common.ArgParser()
    parser.add_argument('--output', '-o', default='', help='output_filename')
    args = parser.parse_args()

    file_events = {label: parse_file(file, args.delimiter)
                   for label, file in extract_label_file(args.file)}
    filename = args.output or '_'.join(file_events.keys())
    filename = filename + '.csv'
    merge_csv(file_events, filename)
