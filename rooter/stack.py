class Stack:
    def __init__(self):
        self.__stack = []

    def isEmpty(self):
        return self.__stack == []

    def stack(self, element):
        self.__stack.append(element)

    def depile(self):
        if not self.isEmpty():
            return self.__stack.pop()
        
    def get(self):
        return self.__stack