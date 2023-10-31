from rooter import rooter

class Table:
    def __init__(self, title=None, border=False):
        self.__title = title
        self.__border = border
        self.__columns = []
        self.__rows = []

    def setColumns(self, *columns):
        column_to_add = []
        for element in columns:
            column_to_add.append(element)
        self.__columns = column_to_add

    def addColumn(self, column):
        self.__columns.append(column)

    def addRow(self, *row):
        row_to_add = []
        for element in row:
            row_to_add.append(element)
        self.__rows.append(row_to_add)

    def __str__(self):
        table = []

        # Calcul of columns' size
        length_columns = [len(column) for column in self.__columns] if self.__columns else [0 for i in self.__rows]
        for row in self.__rows:
            for i in range(len(row)):
                if len(row[i]) > length_columns[i]:
                    length_columns[i] = len(row[i])
        length_columns = [length + 2 for length in length_columns]
        
        # Creation of columns
        if self.__columns != []:
            # Top of column
            top_column = '┏'
            content_column = '┃'
            bottom_column = '┡'
            for i in range(len(length_columns)):
                # Top of column
                top_column += '━' * length_columns[i]
                top_column += '┳' if i != len(length_columns) - 1 else '┓'

                # Content of column
                content_column += ' ' + self.__columns[i] + ' ' * (length_columns[i] - len(self.__columns[i]) - 1) + '┃'

                # Bottom of column
                bottom_column += '━' * length_columns[i]
                bottom_column += '╇' if i != len(length_columns) - 1 else '┩'

            table.append(top_column)
            table.append(content_column)
            table.append(bottom_column)
        else:
            # Top of column
            top_column = '┌'
            for i in range(len(length_columns)):
                top_column += '─' * length_columns[i]
                top_column += '┬' if i != len(length_columns) - 1 else '┐'
            table.append(top_column)

        # Creation of rows
        for i in range(len(self.__rows)):
            content = '│'
            for element in range(len(self.__rows[i])):
                content += ' ' + self.__rows[i][element] + ' ' * (length_columns[element] - len(self.__rows[i][element]) - 1) + '│'
            table.append(content)

            if self.__border and i != len(self.__rows) - 1:
                content = '├'
                for element in range(len(self.__rows[i])):
                    content += '─' * length_columns[element]
                    content += '┼' if element != len(self.__rows[i]) - 1 else '┤'
                table.append(content)

        # Creation of bottom
        bottom = '└'
        for i in range(len(length_columns)):
            bottom += '─' * length_columns[i]
            bottom += '┴' if i != len(length_columns) - 1 else '┘'
        table.append(bottom)

        # Creation of title
        if self.__title:
            half = (len(table[0]) - len(self.__title)) // 2
            table.insert(0, ' ' * half + self.__title)

        return '\n'.join(table)