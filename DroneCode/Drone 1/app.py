from tello import Tello
import sys
from datetime import datetime
import time
import argparse

def parse_args(args):
    """
    Parses arguments.
    :param args: Arguments.
    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser('Tello Flight Commander', 
        epilog='One-Off Coder https://www.oneoffcoder.com')

    parser.add_argument('-f', '--file', help='command file', required=True)
    return parser.parse_args(args)


def start(file_name):
    """
    Starts sending commands to Tello.
    :param file_name: File name where commands are located.
    :return: None.
    """
    start_time = str(datetime.now())

    with open(file_name, 'r') as f:
        commands = f.readlines()

    tello = Tello()
    for command in commands:
        if command != '' and command != '\n':
            command = command.rstrip()

            if command.find('poly') != -1:
                sides = int(command.partition('poly')[2])
                for s in range(sides):
                    command= "forward 25" #to update 
                    tello.send_command(command)
                    command2= (f"ccw {(round(360/sides))}")
                    tello.send_command(command2)
                pass

            else:
                tello.send_command(command)

    with open(f'log/{start_time}.txt', 'w') as out:
        log = tello.get_log()

        for stat in log:
            stat.print_stats()
            s = stat.return_stats()
            out.write(s)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    file_name = args.file
    start(file_name)
