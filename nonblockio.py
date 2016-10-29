
from sys import stdin
from time import sleep
from select import select

def nonblockinput(prompt=''):
    pass


def stdin_ready():
    """
    Return True if STDIN contains data that can be used as input.
    Check this function before reading input to ensure that input will not block.
    """
    ready, _, _ = select([stdin], [], [], 0.0)
    return stdin in ready


def test():
    while True:
        if stdin_ready():
            data = input()
            print("You entered: '{}'.".format(data))
        else:
            print('.', end='', flush=True)
            sleep(0.2)


if __name__ == '__main__':
    test()
