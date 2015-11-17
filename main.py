import colorama as color

color.init()

RESET = color.Fore.RESET + color.Back.RESET + color.Style.RESET_ALL;


def green(text):
    print(color.Fore.GREEN + text + RESET)

"""
print(color.Fore.RED + 'some red text')
print(color.Back.GREEN + 'and with a green background')
print(color.Style.DIM + 'and in dim text')
print(color.Fore.RESET + color.Back.RESET + color.Style.RESET_ALL)
print('back to normal now')
"""

green("Test")
print("Huch?")