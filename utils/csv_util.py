class CsvBuilder:
    def __init__(self):
        self.rows = []

    def add_row(self, list):
        self.rows.append(','.join(list))

    def add_header_end(self):
        return self.rows.append('-----')

    def dump(self):
        return '\n'.join(self.rows)

    @staticmethod
    def span_row(text, nrows):
        return text + '|' * nrows

    @staticmethod
    def span_col(text, ncols):
        return text + '-' * ncols
