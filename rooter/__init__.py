import builtins

# class: Rooter
class Rooter:
    def __init__(self):
        self.tags = [
            {'start': '<b>', 'end': '</b>', 'value': '\033[1m'},
            {'start': '<u>', 'end': '</u>', 'value': '\033[4m'}
        ]

        self.styles = {
            'bold': '\033[1m'
        }

        self.colors = {}

rooter = Rooter()

# function: print
def print(message, styles=False):
    if isinstance(message, str):
        for tag in rooter.tags:
            while tag['start'] in message:
                start_index = message.find(tag['start']) + len(tag['start'])
                end_index = message.find(tag['end'])
                edit = message[start_index:end_index]
                message = message.replace(tag['start'] + edit + tag['end'], tag['value'] + edit + '\033[0m')
    elif isinstance(message, bool):
        message = '\033[32m' + str(message) + '\033[0m' if message else '\033[31m' + str(message) + '\033[0m'
    elif message == None:
        message = '\033[35m' + str(message) + '\033[0m'
    elif isinstance(message, float) or isinstance(message, int):
        message = '\033[36m' + str(message) + '\033[0m'

    if styles:
        style_to_add = ""
        for style, value in rooter.styles.items():
            if style in styles.split(' '):
                style_to_add += value

        message = style_to_add + message + '\033[0m'

    builtins.print(message)