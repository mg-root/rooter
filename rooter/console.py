from rooter import print
import os

class Console:
    def __init__(self, prompt, commands_folder):
        self.__prompt = prompt
        self.__commands_folder = commands_folder
        self.__commands = {}

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
        while True:
            command = input('\n' + self.__prompt)
            self.processCommand(command)
    
    def processCommand(self, command):
        command_name, *arguments = command.split(' ')
        if command_name in self.__commands:
            command = self.__commands[command_name]
        
            overwritten_arguments = {}
            if command['arguments']:
                arguments_names = ""
                for k in command['arguments'].keys():
                    arguments_names += f" [{k}]"

                if len(arguments) < len(command['arguments']):
                    return print(f"<red>[!] Correct use:</red> <yellow>{command_name}{arguments_names}<yellow/>")

                i = 0
                for k,v in command['arguments'].items():
                    if v == 'string' and arguments[i] != '':
                        overwritten_arguments[k] = arguments[i]
                    elif v == 'string+' and arguments[i] != '':
                        overwritten_arguments[k] = ' '.join(arguments[i:])
                    elif v == 'int' and arguments[i].isdigit():
                        overwritten_arguments[k] = int(arguments[i])
                    else:
                        return print(f"<red>[!] Correct use:</red> <yellow>{command_name}{arguments_names}<yellow/>")
                    i+=1

            if command_name == 'help':
                command['execute'](self, arguments)
            else:
                command['execute'](overwritten_arguments)
        else:
            print(f"<red>The command <yellow>{command_name}</yellow> doesn't exist.</red>")