from enum import Enum

CLEAR_SCREEN = "\033[2J"
def goto(i: int, j: int) -> str:
    return f'\033[{i};{j}f'

class AnsiColor(Enum):
    RESET     = '\033[0m'
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    MAGENTA   = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
