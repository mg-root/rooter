from rooter import rooter, print, formatText
from getpass import getpass
import builtins

class Prompt:
    def __init__(self, text, password=False, default=None, type=str, choices=None, between=None, color_input='', invalid_input_text='<red>Incorrect input.</>'):
        self.__text = text
        self.__password = password
        self.__default = default
        self.__type = type
        self.__choices = choices
        self.__between = between.split('-') if between else between
        self.__color_input = rooter.getColor(color_input)
        self.__invalid_input_text = formatText(invalid_input_text)

    def ask(self):
        while True:
            default = rooter.getColor('cyan') + f" [Default: {self.__default}]" + rooter.reset if self.__default else ''
            choice = rooter.getColor('purple') + f" [Choices: {' / '.join(self.__choices)}]" + rooter.reset if self.__choices else ''
            prompt = input(f"{self.__text}{default}{choice} : {self.__color_input}") if not self.__password else getpass(f"{self.__text}{default}{choice} : ")
            builtins.print(rooter.reset, end='')

            if self.__default and prompt == '':
                return self.__default

            check_type = True if self.__type == str or self.__type == None or (self.__type == int and prompt.isdigit()) else False
            if self.__type == float:
                try:
                    float(prompt)
                    check_type = True
                except:
                    check_type = False

            check_choice = True if not self.__choices or (self.__choices and prompt in self.__choices) else False

            check_between = True if not self.__between or (self.__between and self.__between[0] <= prompt <= self.__between[1]) else False

            if check_choice and check_type and check_between:
                if self.__type == int:
                    return int(prompt)
                elif self.__type == float:
                    return float(prompt)
                else:
                    return prompt
            else:
                print(self.__invalid_input_text)