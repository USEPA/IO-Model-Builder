import colorama as color
import traceback

color.init()


def info(message):
    m = '  INFO: ' + message
    __log(m, None)


def warn(message):
    m = '  WARNING: ' + message
    __log(m, color.Fore.YELLOW)


def error(message, err=None):
    m = '  ERROR: ' + message
    __log(m, color.Fore.RED)
    if err is not None:
        traceback.print_tb(err.__traceback__)


def __log(message, col=None):
    if col is None:
        print(message)
    else:
        print(col + message + color.Fore.RESET)
