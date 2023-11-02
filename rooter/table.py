from rooter import rooter, getLengthWithoutTags, formatText

class Table:
    def __init__(self, title=None, border=False, border_color=''):
        self.__title = title
        self.__border = border
        self.__border_color = rooter.getColor(border_color)
        self.__columns = []
        self.__rows = []

    def setColumns(self, *columns):
        column_to_add = []
        for element in columns:
            column_to_add.append(element)
        self.__columns = column_to_add

    def addColumn(self, column, styles=''):
        styles_to_add = ''
        for style in styles.split(' '):
            styles_to_add += rooter.getColor(style) if rooter.getStyle(style) == '' else rooter.getStyle(style)
        self.__columns.append([column, styles_to_add])

    def addRow(self, *row):
        if type(row[0]) == list:
            self.__rows.append([str(element) for element in row[0]])
        else:
            row_to_add = []
            for element in row:
                row_to_add.append(str(element))
            self.__rows.append(row_to_add)

    def __str__(self):
        table = []

        # Calcul of columns' size
        length_columns = [getLengthWithoutTags(column[0]) for column in self.__columns] if self.__columns else [0 for i in self.__rows]
        for row in self.__rows:
            for i in range(len(row)):
                if getLengthWithoutTags(row[i]) > length_columns[i]:
                    length_columns[i] = getLengthWithoutTags(row[i])
        length_columns = [length + 2 for length in length_columns]
        
        # Creation of columns
        if self.__columns != []:
            # Top of column
            top_column = self.__border_color + '┏'
            content_column = self.__border_color + '┃' + rooter.reset
            bottom_column = self.__border_color + '┡'
            for i in range(len(length_columns)):
                # Top of column
                top_column += '━' * length_columns[i]
                top_column += '┳' if i != len(length_columns) - 1 else '┓' + rooter.reset

                # Content of column
                length = getLengthWithoutTags(self.__columns[i][0])
                text = formatText(self.__columns[i][0])
                content_column += ' ' + text + ' ' * (length_columns[i] - length - 1) + self.__border_color + '┃' + rooter.reset

                # Bottom of column
                bottom_column += '━' * length_columns[i]
                bottom_column += '╇' if i != len(length_columns) - 1 else '┩' + rooter.reset

            table.append(top_column)
            table.append(content_column)
            table.append(bottom_column)
        else:
            # Top of column
            top_column = self.__border_color + '┌'
            for i in range(len(length_columns)):
                top_column += '─' * length_columns[i]
                top_column += '┬' if i != len(length_columns) - 1 else '┐' + rooter.reset
            table.append(top_column)

        # Creation of rows
        for i in range(len(self.__rows)):
            content = self.__border_color + '│' + rooter.reset
            column = 0
            for element in range(len(self.__rows[i])):
                length = getLengthWithoutTags(self.__rows[i][element])
                text = formatText(self.__rows[i][element])
                content += ' ' + self.__columns[column][1] + text + rooter.reset + ' ' * (length_columns[element] - length - 1) + self.__border_color + '│' + rooter.reset if self.__columns != [] else ' ' + text + ' ' * (length_columns[element] - length - 1) + self.__border_color + '│' + rooter.reset
                column += 1
            table.append(content)

            if self.__border and i != len(self.__rows) - 1:
                content = self.__border_color + '├'
                for element in range(len(self.__rows[i])):
                    content += '─' * length_columns[element]
                    content += '┼' if element != len(self.__rows[i]) - 1 else '┤' + rooter.reset
                table.append(content)

        # Creation of bottom
        bottom = self.__border_color + '└'
        for i in range(len(length_columns)):
            bottom += '─' * length_columns[i]
            bottom += '┴' if i != len(length_columns) - 1 else '┘' + rooter.reset
        table.append(bottom)

        # Creation of title
        if self.__title:
            length = getLengthWithoutTags(self.__title)
            text = formatText(self.__title)
            length_line = sum([length for length in length_columns]) + len(length_columns)
            half = (length_line - length) // 2
            table.insert(0, ' ' * half + text)

        return '\n'.join(table)