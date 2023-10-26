import time, sys

class Progress:
    def __init__(self, title=None):
        self.__title = title

    def start(self):
        for i in range(100):
            time.sleep(0.1)
            progress = (i + 1) / 100
            progress_percent = int(progress * 100)

            sys.stdout.write("\r[" + "#" * progress_percent + " " * (100 - progress_percent) + f"] {progress_percent}%")
            sys.stdout.flush()