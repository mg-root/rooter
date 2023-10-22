from rooter import rooter

class Table:
    def __init__(self, title=None):
        self.__title = title
        self.__columns = []
        self.__rows = []
        self.__lengths = []

    def addColumn(self, column: str):
        self.__columns.append(column)

    def addRow(self, row: list):
        self.__rows.append(row)

    def __str__(self):
        self.__lengths = ["1111111111"]
        
        table = []

        top = '┏'
        for i in range(len(self.__lengths)):
            top += '━' * self.__lengths[i]
            top += '┳' if i < len(self.__lengths) - 1 else '┓'
        table.append(top)

        return '\n'.join(table)