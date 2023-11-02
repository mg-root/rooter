from rooter import print, formatText
from rooter.table import Table
import json, os

classes = {
    str: 'str',
    int: 'int',
    float: 'float',
    bool: 'bool',
    list: 'list',
    dict: 'dict',
    tuple: 'tuple'
}

accept_classes = ['str', 'int', 'float', 'bool', 'list', 'dict', 'tuple']

class Model:
    def __init__(self, table, model=None):
        self.__table = table
        self.__model = model
        os.mkdir('database') if not os.path.exists('database') else None

    def create(self):
        for key, settings in self.__model.items():
            if 'type' not in settings:
                raise TypeError(formatText(f"<red>The setting <yellow>type</> is missing for <yellow>{key}</>.</>"))
            elif settings['type'] not in accept_classes:
                raise TypeError(formatText(f"<red>The type <yellow>{settings['type']}</> isn't accepted or doesn't exist.</>"))
            elif 'auto_increment' in settings and settings['auto_increment'] and settings['type'] != 'int':
                raise TypeError(formatText(f"<red>The type of <yellow>{key}</> must be <yellow>int</>.</>"))
            elif 'default' in settings:
                if classes[type(settings['default'])] != settings['type']:
                    raise TypeError(formatText(f"<red>The default value doesn't match with the type for <yellow>{key}</>.</>"))
                if 'primary' in settings or 'auto_increment' in settings:
                    raise ValueError(formatText(f"<red>You can't set default value to <yellow>{key}</> because it's primary key.</>"))

        data = self.__loadModel()
        data[self.__table] = self.__model
        self.__saveModel(data)

    def delete(self):
        data = self.__loadModel()
        if self.__table in data:
            del data[self.__table]
        else:
            print(f"<red>This model <yellow>{self.__table}</> doesn't exist.</>")

    def __loadModel(self):
        try:
            with open('database/__models.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
            
    def __saveModel(self, data):
        with open('database/__models.json', 'w') as file:
            json.dump(data, file, indent=4)

class JsonDatabase:
    def __init__(self, table_name):
        self.__table_name = table_name
        if not os.path.exists('database/__models.json'):
            raise FileNotFoundError('You must create a model of the table before.')
        else:
            with open('database/__models.json', 'r') as file:
                self.__model = json.load(file)

        os.mkdir('database') if not os.path.exists('database') else None
        if table_name not in self.__model:
            raise FileExistsError('You must create a model of the table before.')
        else:
            self.__model = self.__model[self.__table_name]

    def show(self, where=None, order_by=None):
        data = self.__loadData()
        table = Table(title=f"Table: {self.__table_name}")
        for key in self.__model:
            styles = 'bold underline' if ('primary' in self.__model[key] and self.__model[key]['primary']) or 'auto_increment' in self.__model[key] and self.__model[key]['auto_increment'] else 'cyan' if self.__model[key]['type'] == 'int' or self.__model[key]['type'] == float else 'green' if self.__model[key]['type'] == 'str' else ''
            table.addColumn(key, styles=styles)

        if order_by:
            order_by = [element for element in order_by.split(' ') if element != '']
            if order_by[0] == 'ASC' or order_by[0] == 'DESC':
                if order_by[1] in self.__model:
                    if len(data) > 1:
                        if order_by[0] == 'ASC':
                            data = sorted(data, key=lambda x: x[order_by[1]])
                        elif order_by[0] == 'DESC':
                            data = sorted(data, key=lambda x: x[order_by[1]], reverse=True)
                        else:
                            raise ValueError(formatText(f"<red>The option <yellow>{order_by[0]}</> isn't correct. Must be <yellow>ASC or DESC</>.</>"))
                else:
                    raise ValueError(formatText(f"<red>The key <yellow>{order_by[1]}</> isn't in the table <yellow>{self.__table_name}</>.</>")) 
                
        if where:
            where, operator = self.__condition(where)
            where[1] = int(where[1]) if self.__model[where[0]]['type'] == 'int' else float(where[1]) if self.__model[where[0]]['type'] == 'float' else where[1] 
            if where[0] not in self.__model:
                raise ValueError(formatText(f"<red>This key <yellow>{where[0]}</> isn't correct.</>"))
            
            index_list = []
            for i in range(len(data)):
                if operator == '=' and data[i][where[0]] == where[1]:
                    index_list.append(i)
                elif operator == '>=':
                    if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                        if data[i][where[0]] >= where[1]:
                            index_list.append(i)
                elif operator == '<=':
                    if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                        if data[i][where[0]] <= where[1]:
                            index_list.append(i)
                elif operator == '>':
                    if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                        if data[i][where[0]] > where[1]:
                            index_list.append(i)
                elif operator == '<':
                    if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                        if data[i][where[0]] < where[1]:
                            index_list.append(i)
                elif operator == '!=' and data[i][where[0]] != where[1]:
                    index_list.append(i)

            rows = []
            for i in index_list:
                row = []
                for key in self.__model:
                    row.append(f"<purple>{data[i][key]}</>") if data[i][key] == None else row.append(f"<white>{data[i][key]}</>") if ('primary' in self.__model[key] and self.__model[key]['primary']) or ('auto_increment' in self.__model[key] and self.__model[key]['auto_increment']) else row.append(f"<green><bold>{data[i][key]}</></>") if data[i][key] == True else row.append(f"<red><bold>{element[key]}</></>") if data[i][key] == False  else row.append(data[i][key])
                rows.append(row)
        
            for row in rows:
                table.addRow(row)
        else:            
            rows = []
            for element in data:
                row = []
                for key in self.__model:
                    row.append(f"<purple>{element[key]}</>") if element[key] == None else row.append(f"<white>{element[key]}</>") if ('primary' in self.__model[key] and self.__model[key]['primary']) or ('auto_increment' in self.__model[key] and self.__model[key]['auto_increment']) else row.append(f"<green><bold>{element[key]}</></>") if element[key] == True else row.append(f"<red><bold>{element[key]}</></>") if element[key] == False  else row.append(element[key])
                rows.append(row)

            for row in rows:
                table.addRow(row)

        print(table)

    def get(self, where=None, order_by=None):
        data = self.__loadData()
        got_data = []

        if order_by:
            order_by = [element for element in order_by.split(' ') if element != '']
            if order_by[0] == 'ASC' or order_by[0] == 'DESC':
                if order_by[1] in self.__model:
                    if len(data) > 1:
                        if order_by[0] == 'ASC':
                            data = sorted(data, key=lambda x: x[order_by[1]])
                        elif order_by[0] == 'DESC':
                            data = sorted(data, key=lambda x: x[order_by[1]], reverse=True)
                        else:
                            raise ValueError(formatText(f"<red>The option <yellow>{order_by[0]}</> isn't correct. Must be <yellow>ASC or DESC</>.</>"))
                else:
                    raise ValueError(formatText(f"<red>The key <yellow>{order_by[1]}</> isn't in the table <yellow>{self.__table_name}</>.</>")) 

        if where:
            where, operator = self.__condition(where)
            where[1] = int(where[1]) if self.__model[where[0]]['type'] == 'int' else float(where[1]) if self.__model[where[0]]['type'] == 'float' else where[1] 
            if where[0] not in self.__model:
                raise ValueError(formatText(f"<red>This key <yellow>{where[0]}</> isn't correct.</>"))
            
            index_list = []
            for i in range(len(data)):
                if operator == '=' and data[i][where[0]] == where[1]:
                    index_list.append(i)
                elif operator == '>=':
                    if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                        if data[i][where[0]] >= where[1]:
                            index_list.append(i)
                elif operator == '<=':
                    if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                        if data[i][where[0]] <= where[1]:
                            index_list.append(i)
                elif operator == '>':
                    if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                        if data[i][where[0]] > where[1]:
                            index_list.append(i)
                elif operator == '<':
                    if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                        if data[i][where[0]] < where[1]:
                            index_list.append(i)
                elif operator == '!=' and data[i][where[0]] != where[1]:
                    index_list.append(i)

            for i in index_list:
                got_data.append(data[i])

            return got_data if len(got_data) > 1 else got_data[0]
        else:
            return data

    def insert(self, keys=[], values=[]):
        data = self.__loadData()
        insert_data = {}
        
        for index in range(len(keys)):
            if keys[index] in self.__model:
                key = keys[index]
                settings = self.__model[key]
                if 'primary' in settings and settings['primary']:
                    if self.__check_class(key, values[index], settings['type']):
                        for element in data:
                            if element[key] == values[index]:
                                raise ValueError(formatText('<red>Double value for a primary key.</>'))
                        insert_data[key] = values[index]
                elif 'auto_increment' in settings and settings['auto_increment']:
                    if type(values[index]) == int:
                        for element in data:
                            if element[index] == values[index]:
                                raise ValueError(formatText('<red>Double value for a primary key about auto increment.</>'))
                        insert_data[key] = values[index]
                elif self.__check_class(key, values[index], settings['type']):
                    insert_data[key] = values[index]

        missing_keys = [key for key in self.__model if key not in insert_data]
        
        for key in missing_keys:
            settings = self.__model[key]
            if 'primary' in settings and settings['primary']:
                raise ValueError(formatText(f"<red>You must set a value for <yellow>{key}</> because it's a primary key.</>"))
            elif 'auto_increment' in settings and settings['auto_increment']:
                i = 1
                for element in data:
                    if element[key] == i:
                        i += 1
                insert_data[key] = i
            elif 'default' in settings:
                insert_data[key] = settings['default']
            else:
                insert_data[key] = None

        data.append(insert_data)
        self.__saveData(data)

    def update(self, key, value, where):
        data = self.__loadData()

        where, operator = self.__condition(where)
        where[1] = int(where[1]) if self.__model[where[0]]['type'] == 'int' else float(where[1]) if self.__model[where[0]]['type'] == 'float' else where[1] 
        if where[0] not in self.__model:
            raise ValueError(formatText(f"<red>This key <yellow>{where[0]}</> isn't correct.</>"))
            
        index_list = []
        for i in range(len(data)):
            if operator == '=' and data[i][where[0]] == where[1]:
                index_list.append(i)
            elif operator == '>=':
                if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                    if data[i][where[0]] >= where[1]:
                        index_list.append(i)
            elif operator == '<=':
                if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                    if data[i][where[0]] <= where[1]:
                        index_list.append(i)
            elif operator == '>':
                if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                    if data[i][where[0]] > where[1]:
                        index_list.append(i)
            elif operator == '<':
                if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                    if data[i][where[0]] < where[1]:
                        index_list.append(i)
            elif operator == '!=' and data[i][where[0]] != where[1]:
                index_list.append(i)

        if index_list:
            if key in self.__model:
                if self.__check_class(key, value, self.__model[key]['type']):
                    for i in index_list:
                        data[i][key] = value
                    self.__saveData(data)
            else:
                raise ValueError(formatText(f"<red>The key <yellow>{key}</> isn't in the table <yellow>{self.__table_name}</>.</>"))
        else:
            raise ValueError(formatText(f"<red>This key <yellow>{where[0]} = {where[1]}</> matches with no element the table <yellow>{self.__table_name}</>.</>"))

    def delete(self, where):
        data = self.__loadData()
        
        where, operator = self.__condition(where)
        where[1] = int(where[1]) if self.__model[where[0]]['type'] == 'int' else float(where[1]) if self.__model[where[0]]['type'] == 'float' else where[1] 
        if where[0] not in self.__model:
            raise ValueError(formatText(f"<red>This key <yellow>{where[0]}</> isn't correct.</>"))
            
        index_list = []
        for i in range(len(data)):
            if operator == '=' and data[i][where[0]] == where[1]:
                index_list.append(i)
            elif operator == '>=':
                if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                    if data[i][where[0]] >= where[1]:
                        index_list.append(i)
            elif operator == '<=':
                if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                    if data[i][where[0]] <= where[1]:
                        index_list.append(i)
            elif operator == '>':
                if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                    if data[i][where[0]] > where[1]:
                        index_list.append(i)
            elif operator == '<':
                if type(data[i][where[0]]) == int or type(data[i][where[0]]) == float:
                    if data[i][where[0]] < where[1]:
                        index_list.append(i)
            elif operator == '!=' and data[i][where[0]] != where[1]:
                index_list.append(i)

        if index_list:
            for i in sorted(index_list, reverse=True):
                del data[i]
            self.__saveData(data)
        else:
            raise ValueError(formatText(f"<red>This key <yellow>{where[0]} = {where[1]}</> matches with no element in the table <yellow>{self.__table_name}</>.</>"))

    def __check_class(self, key, value, value_type):
        if classes[type(value)] == value_type:
            return True
        else:
            raise TypeError(formatText(f"<red>The type of <yellow>{key}</> isn't correct.</>"))

    def __condition(self, text):
        if '>=' in text:
            return [element.replace(' ', '') for element in text.split('>=')], '>='
        elif '<=' in text:
            return [element.replace(' ', '') for element in text.split('<=')], '<='
        elif '>' in text:
            return [element.replace(' ', '') for element in text.split('>')], '>'
        elif '<' in text:
            return [element.replace(' ', '') for element in text.split('<')], '<'
        elif '!=' in text:
            return [element.replace(' ', '') for element in text.split('!=')], '!='
        elif '=' in text:
            return [element.replace(' ', '') for element in text.split('=')], '='
        else:
            raise ValueError(formatText(f"<red>There is a problem with your condition: <yellow>{text}</>.</>"))

    def __loadData(self):
        try:
            with open(f'database/{self.__table_name}.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        
    def __saveData(self, data):
        with open(f'database/{self.__table_name}.json', 'w') as file:
            json.dump(data, file, indent=4)