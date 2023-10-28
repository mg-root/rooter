from rooter import rooter, formatText
import time, sys

class Progress:
    def __init__(self, title='', width=25, duration=10):
        self.__title = ' ' + title if title != '' else ''
        self.__width = width
        self.__duration = duration

    def start(self):
        load = ['∴', '∶', '∵', '∷']
        start_time = time.time()

        for i in range(100):
            time.sleep(0.1)
            elapsed_time = time.time() - start_time
            progress = elapsed_time / self.__duration
            progress_percent = int(progress * 100)
            progress_chars = int(progress * self.__width)
            remaining_time = round(self.__duration - elapsed_time, 1)

            hours = int(remaining_time / 3600)
            minutes = int((remaining_time % 3600) / 60)
            seconds = int(remaining_time % 60)
            remaining_time_str = f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"

            sys.stdout.write('\r' + rooter.getColor('green') + load[i % len(load)]  + rooter.reset + formatText(self.__title) + ' ' + rooter.getColor('red') + '━' * progress_chars + rooter.getColor('grey') + '━' * (self.__width - progress_chars) + f" {rooter.getColor('purple')}{progress_percent}%{rooter.getColor('cyan')} {remaining_time_str}{rooter.reset}")
            sys.stdout.flush()

            if progress_percent >= 100:
                progress_percent = 100
                sys.stdout.write('\r' + '✅' + formatText(self.__title) + ' ' + rooter.getColor('green') + '━' * progress_chars + rooter.getColor('grey') + '━' * (self.__width - progress_chars) + f" {rooter.getColor('purple')}{progress_percent}%{rooter.getColor('cyan')} 00:00:00{rooter.reset}")
                break

        print()
        return True