import builtins
def print(message):
    if isinstance(message, str):
        tags = [
            {'start': '<b>', 'end': '</b>', 'value': '\033[1m'}
        ]

        for tag in tags:
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
    builtins.print(message)