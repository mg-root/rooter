from rooter import print, formatText, rooter
import os, builtins

class CLI:
    def __init__(self, prompt='> ', color_input='', commands_folder='commands', help_command=False, addons=[]):
        self.__prompt = formatText(prompt)
        self.__color_input = rooter.getColor(color_input)
        self.__commands_folder = commands_folder
        self.__help_command = help_command
        self.__addons = addons
        self.__commands = {}
        self.__display = True

    def loadCommands(self):
        for file in os.listdir(self.__commands_folder):
            if os.path.isfile(f"{self.__commands_folder}/{file}"):
                command = {}

                with open(f"{self.__commands_folder}/{file}", 'r') as python_file:
                    exec(python_file.read(), command)
                python_file.close()

                self.__commands[command['name']] = {
                    'description': command['description'],
                    'arguments': command['arguments'],
                    'execute': command['execute']
                }

    def getCommands(self):
        return self.__commands

    def display(self):
        self.__display = True
        while self.__display:
            command = input('\n' + self.__prompt + self.__color_input)
            builtins.print(rooter.reset, end='')
            self.__processCommand(command)

    def stop(self):
        self.__display = False
    
    def __processCommand(self, command):
        command_name, *arguments = command.split(' ')
        if command_name in self.__commands:
            command = self.__commands[command_name]
        
            overwritten_arguments = {}
            if command['arguments']:
                arguments_names = ""
                for k in command['arguments'].keys():
                    arguments_names += f" [{k}]"

                if len(arguments) < len(command['arguments']):
                    return print(f"<red>[!] Correct use:</> <yellow>{command_name}{arguments_names}</>")

                i = 0
                for k,v in command['arguments'].items():
                    if v == 'string' and arguments[i] != '':
                        overwritten_arguments[k] = arguments[i]
                    elif v == 'string+' and arguments[i] != '':
                        overwritten_arguments[k] = ' '.join(arguments[i:])
                    elif v == 'int' and arguments[i].isdigit():
                        overwritten_arguments[k] = int(arguments[i])
                    else:
                        return print(f"<red>[!] Correct use:</> <yellow>{command_name}{arguments_names}</>")
                    i+=1

            if command_name == 'help':
                command['execute'](self, arguments)
            else:
                command['execute'](self, overwritten_arguments, *self.__addons)
        elif self.__help_command and command_name == 'help':
            init_length = 0
            for name in self.__commands.keys():
                if len(name) > init_length:
                    init_length = len(name)
            length = init_length
            for name in self.__commands:
                usage = ''
                if self.__commands[name]['arguments']:
                    for argument in self.__commands[name]['arguments'].keys():
                        usage += f' <{argument}>'
                    if len(usage) + len(name) > length:
                        length = len(usage) + len(name)
    
            for name in self.__commands:
                usage = ''
                if self.__commands[name]['arguments']:
                    for argument in self.__commands[name]['arguments'].keys():
                        usage += f' <{argument}>'
                builtins.print(f"{name}{usage}{' ' * (length - (len(name) + len(usage)))} | {self.__commands[name]['description']}") 
        else:
            print(f"<red>The command <yellow>{command_name}</> doesn't exist.</>")