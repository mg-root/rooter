import builtins, os

# class: Rooter
class Rooter:
    def __init__(self):
        self.reset = '\033[0m'

        self.tags = [
            {'start': '<reset>', 'end': '</reset>', 'value': self.reset}
        ]

        self.styles = {
            'b': '\033[1m',
            'dim': '\033[2m',
            'i': '\033[3m',
            'u': '\033[4m',
            's': '\033[9m',
            'r': '\033[7m'
        }

        self.colors = {
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'magenta': '\033[35m',
            'purple': '\033[38;2;154;4;237m',
            'cyan': '\033[36m',
            'white': '\033[37m',

            'bg_black': '\033[40m',
            'bg_red': '\033[41m',
            'bg_green': '\033[42m', 
            'bg_yellow': '\033[43m', 
            'bg_blue': '\033[44m', 
            'bg_magenta': '\033[45m', 
            'bg_cyan': '\033[46m', 
            'bg_white': '\033[47m'
        }

        for name, style in self.styles.items():
            self.tags.append({'start': f'<{name}>', 'end': f'</{name}>', 'value': style})

        for name, color in self.colors.items():
            self.tags.append({'start': f'<{name}>', 'end': f'</{name}>', 'value': color})

    def addColor(self, name, hex=False, rgb=False):
        if name in self.colors:
            raise ValueError('This color already exists.')
        elif hex:
            hex_color = hex.lstrip('#')
            color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            self.colors[name] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m'
            self.tags.append({'start': f'<{name}>', 'end': f'</{name}>', 'value': self.colors[name]})
        elif rgb:
            r,g,b = rgb
            self.colors[name] = f'\033[38;2;{r};{g};{b}m'
            self.tags.append({'start': f'<{name}>', 'end': f'</{name}>', 'value': self.colors[name]})

    def getColor(self, name):
        return self.colors[name] if name in self.colors else ''

rooter = Rooter()

# function: print
def print(message, styles=False):
    if isinstance(message, str):
        for tag in rooter.tags:
            while tag['start'] in message:
                start_index = message.find(tag['start']) + len(tag['start'])
                if tag['end'] in message:
                    end_index = message.find(tag['end'])
                    edit = message[start_index:end_index]
                    message = message.replace(tag['start'] + edit + tag['end'], tag['value'] + edit + rooter.reset)
                else:
                    message = message.replace(tag['start'] + message[start_index], tag['value'] + message[start_index])
    elif isinstance(message, bool):
        message = rooter.colors['green'] + rooter.styles['i'] + str(message) + rooter.reset if message else rooter.colors['red'] + rooter.styles['i'] + str(message) + rooter.reset
    elif message == None:
        message = rooter.colors['purple'] + rooter.styles['i'] + str(message) + rooter.reset
    elif isinstance(message, float) or isinstance(message, int):
        message = rooter.colors['cyan'] + str(message) + rooter.reset

    if styles:
        style_to_add = ""
        for style, value in rooter.styles.items():
            if style in styles.split(' '):
                style_to_add += value

        for color, value in rooter.colors.items():
            if color in styles.split(' '):
                style_to_add += value

        message = style_to_add + message + rooter.reset

    builtins.print(message)

# function: clear
def clear():
    os.system('cls')