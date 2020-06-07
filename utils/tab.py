import re

css = '''
body {
  margin: 0;
}
table {
  width: max-content;
  border-spacing: 1;
  border-collapse: collapse;
  background: white;
  overflow: hidden;
  margin: 0 auto;
  font-size: 13px;
  font-family: Helvetica, Arial, sans-serif;
}
thead tr {
  height: 35px;
  background: #36304a;
}
tbody tr:last-child {
  border: 0;
}
td, th {
  max-width: 190px;
  padding: 5px;
  line-height: 1.3;
  text-align: center;
}
tbody td {
  word-break: break-word;
}
thead th {
  color: #fff;
  font-weight: unset;
}
tbody tr {
  height: 50px;
  color: #808080;
  font-weight: unset;
}
tbody tr:nth-child(even) {
  background-color: #f5f5f5;
}
'''

HTML = '<html><meta charset="utf-8">{}</html>'
TR = '<tr>{}</tr>'
TD = '<td>{}</td>'
TH = '<th colspan="{colspan}" rowspan="{rowspan}">{text}</th>'
HIGHLIGHT = '<b style="color: #f7444e">{}</b>'
STYLE = '<style>{}</style>'
TABLE = '<table><thead>{thead}</thead><tbody>{tbody}</tbody></table>'


def render_cell(content):
    content = content.strip()
    match = re.match(r'^\*([^\*]*)\*$', content)
    if match:
        return HIGHLIGHT.format(match[1])
    return content


def csv2html(csv):
    csv = csv.strip().split('\n')
    thead = ''
    line_idx = 0
    while True:
        line = csv[line_idx].strip()
        if line.startswith('-----'):
            line_idx += 1
            break
        tr_inner = ''
        for col in line.split(','):
            match = re.match(r'\s*(.*?)(-*)(\|*)\s*$', col)
            inner = match[1]
            cspan = len(match[2]) + 1
            rspan = len(match[3]) + 1
            tr_inner += TH.format(colspan=cspan, rowspan=rspan, text=inner)
        thead += TR.format(tr_inner)
        line_idx += 1

    tbody = ''
    for r in csv[line_idx:]:
        tbody += TR.format(''.join([TD.format(render_cell(c)) for c in r.split(',')]))

    stylesheet = STYLE.format(css)
    table = TABLE.format(thead=thead, tbody=tbody)
    return HTML.format(stylesheet + table)


if __name__ == '__main__':
    print(csv2html('a|,b-,c\nd,e,f\n-----\n1,*2*,3,4\n5,6,7,8'))
