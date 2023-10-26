from rooter import rooter

class Panel:
    def __init__(self, title=None, title_color='', text="Panel", color='', border_color='', min_size=None):
        self.__title = title
        self.__title_color = rooter.getColor(title_color) if title_color != '' else rooter.getColor(color)
        self.__text = text
        self.__color = rooter.getColor(color)
        self.__border_color = rooter.getColor(border_color) if border_color != '' else rooter.getColor(color)
        self.__min_size = min_size

    def __str__(self):
        length = len(max(self.__text.split('\n')))
        if self.__min_size and self.__min_size > length:
            length = self.__min_size

        if self.__title and len(self.__title) > length:
            length = len(self.__title) + 2
        panel = []

        panel.append('╭' + '─' * (length + 2) + '╮')
        if self.__title:
            half = (len(panel[0]) - len(self.__title) -2) // 2
            start = panel[0][:half]
            end = panel[0][half + len(self.__title) + 2:]
            panel[0] = start + ' ' + self.__title_color + self.__title + self.__border_color + ' ' + end
        panel[0] = self.__border_color + panel[0] + rooter.reset

        for text in self.__text.split('\n'):
            text_length = len(text)
            text = self.__color + text + rooter.reset
            for tag in rooter.tags:
                while tag['start'] in text:
                    start_index = text.find(tag['start']) + len(tag['start'])
                    text_length -= len(tag['start'])
                    if tag['end'] in text:
                        text_length -= len(tag['end'])
                        end_index = text.find(tag['end'])
                        edit = text[start_index:end_index]
                        text = text.replace(tag['start'] + edit + tag['end'], tag['value'] + edit + rooter.reset)
                    else:
                        text = text.replace(tag['start'] + text[start_index], tag['value'] + text[start_index])
            panel.append(f'{self.__border_color}│{rooter.reset} ' + text + ' ' * (length - text_length) + f' {self.__border_color}│{rooter.reset}')
        panel.append(f'{self.__border_color}╰' + '─' * (length + 2) + '╯' + rooter.reset)

        return '\n'.join(panel)