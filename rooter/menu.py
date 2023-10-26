from rooter.panel import Panel
from rooter.prompt import Prompt
from rooter import print

class Menu:
    def __init__(self, title=None, title_color='', color='', border_color='', color_index='', min_size=None, data=[]):
        self.__title = title
        self.__title_color = title_color
        self.__color = color
        self.__border_color = border_color
        self.__color_index = color_index
        self.__min_size = min_size
        self.__data = data
        
    def setData(self, data: list):
        self.__data = data

    def addData(self, data: str, position=-1):
        self.__data.insert(position, data)

    def show(self):
        text = ''
        for i in range(len(self.__data)):
            text += f"[<{self.__color_index}>{i+1}</{self.__color_index}>] {self.__data[i]}" if self.__color_index != '' else f"[{i+1}] {self.__data[i]}"
            text += '\n' if i != len(self.__data) - 1 else ''

        menu = Panel(title=self.__title, title_color=self.__title_color, text=text, color=self.__color, border_color=self.__border_color, min_size=self.__min_size)
        return print(menu)
    
    def ask(self):
        item = Prompt(text="Choice", type=int, color_input=self.__color_index, between=f'1-{len(self.__data)}', invalid_input_text=f"You have to input a number between <yellow><b>[1]</b><red> and <yellow><b>[{len(self.__data)}]</b><red>.</red>").ask()
        return item - 1