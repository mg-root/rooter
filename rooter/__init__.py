from rooter.stack import Stack
import builtins, os, re, sys

# class: Rooter
class Rooter:
    def __init__(self):
        self.reset = '\033[0m'

        self.tags = {}

        self.styles = {
            'bold': '\033[1m',
            'dim': '\033[2m',
            'italic': '\033[3m',
            'underline': '\033[4m',
            'strikethough': '\033[9m',
            'reverse': '\033[7m'
        }

        self.colors = {
            'black': '\033[30m',
            'grey': '\033[38;2;169;169;169m',
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
            self.tags[name] = style

        for name, color in self.colors.items():
            self.tags[name] = color

    def addColor(self, name, hex=False, rgb=False):
        if name in self.colors:
            print(f'<red>This color name <yellow>{name}</> already exists.</>')
        elif hex:
            hex_color = hex.lstrip('#')
            color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            self.colors[name] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m'
            self.tags[name] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m'
        elif rgb:
            r,g,b = rgb
            self.colors[name] = f'\033[38;2;{r};{g};{b}m'
            self.tags[name] = f'\033[38;2;{r};{g};{b}m'

    def getColor(self, name):
        return self.colors[name] if name in self.colors else ''
    
    def getStyle(self, name):
        return self.styles[name] if name in self.styles else ''

rooter = Rooter()

# function: print
def print(message):
    if isinstance(message, str):
        previous_styles = Stack()
        pattern = re.compile(r'<(.*?)>')
        for match in pattern.finditer(message):
            tag = match.group(1)
            previous_styles.stack(tag) if tag != '/' else None
            if tag == '/':
                tag_depile = previous_styles.depile()
                if not previous_styles.isEmpty():
                    colors = '' if tag_depile not in rooter.styles else rooter.reset
                    for color in previous_styles.get():
                        colors += rooter.tags.get(color)
                    message = message.replace(f"<{tag}>", colors, 1)
                else:
                    message = message.replace(f"<{tag}>", rooter.reset, 1)
            else:
                message = message.replace(f"<{tag}>", rooter.tags.get(tag), 1)
    elif isinstance(message, bool):
        message = rooter.getColor('green') + rooter.getStyle('italic') + str(message) + rooter.reset if message else rooter.getColor('red') + rooter.getStyle('italic') + str(message) + rooter.reset
    elif message == None:
        message = rooter.getColor('purple') + rooter.getStyle('italic') + str(message) + rooter.reset
    elif isinstance(message, float) or isinstance(message, int):
        message = rooter.getColor('cyan') + str(message) + rooter.reset

    builtins.print(message)

# function: getLengthWithoutTags
def getLengthWithoutTags(message):
    length = 0
    pattern = re.compile(r'<(.*?)>')
    for match in pattern.finditer(message):
        tag = match.group(1)
        length += len(f'<{tag}>')
    return len(message) - length

# function: formatText
def formatText(message):
    previous_styles = Stack()
    pattern = re.compile(r'<(.*?)>')
    for match in pattern.finditer(message):
        tag = match.group(1)
        previous_styles.stack(tag) if tag != '/' else None
        if tag == '/':
            tag_depile = previous_styles.depile()
            if not previous_styles.isEmpty():
                colors = '' if tag_depile not in rooter.styles else rooter.reset
                for color in previous_styles.get():
                    colors += rooter.tags.get(color)
                    message = message.replace(f"<{tag}>", colors, 1)
            else:
                message = message.replace(f"<{tag}>", rooter.reset, 1)
        else:
            message = message.replace(f"<{tag}>", rooter.tags.get(tag), 1)
    return message

# function: GroupDigits
def GroupDigits(number, separator=None):
    formatted = '{:,}'.format(number)
    if separator:
        return formatted.replace(',', separator)
    else:
        return formatted.replace(',', ' ')

# function: clear
def clear():
    os.system('cls')

# function: exit
def exit():
    sys.exit()