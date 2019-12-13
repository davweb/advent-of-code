#!/usr/local/bin/python3

from advent.year2019.intcode import IntCode
from collections import defaultdict
from advent import bounds, md5
import curses  
import time

def read_input():
    return [int(code) for code in open('input/2019/day13-input.txt', 'r').read().split(',')]

def part1(code):
    """
    >>> part1(read_input())
    304
    """

    i = IntCode(code, memory_size=10000)
    screen = defaultdict(int)

    while True:
        x = i.execute()

        if x is None:
            break

        y = i.execute()
        square = i.execute()
        screen[(x,y)] = square   

    return sum(1 for key in screen.keys() if screen[key] == 2)


def part2(code, draw):
    """
    >>> part2(read_input(), False)
    14747
    """

    code[0] == 2 
    score = 0
    i = IntCode(code, memory_size=10000)
    screen = defaultdict(int)

    if draw:
        stdscr = curses.initscr()
        curses.curs_set(0)
        stdscr.addstr(24, 0, "Score:")
    
    bat_x = None
    ball_x = None
    playing = False

    while True:
        x = i.execute()

        if x is None:
            if playing:
                break
            playing = True
            continue

        y = i.execute()
        square = i.execute()

        if x == -1 and y == 0:
            score = square

            if draw:
                stdscr.addstr(24, 7, str(score))

            continue 
    
        if square == 3:
            bat_x = x
        elif square == 4:
            ball_x = x

            if not playing:
                joystick = 0
            elif bat_x < ball_x:
                joystick = 1
            elif bat_x > ball_x:
                joystick = -1
            else:
               joystick = 0
               
            i.add_input(joystick)
        
        screen[(x,y)] = square
        
        if draw:
            pixel = [" ","█","▓","▔","•"][square]
            stdscr.addch(y, x, pixel)   
            stdscr.refresh() 

            if (square == 3 or square == 4):
                time.sleep(0.007)  

    if draw:
        curses.endwin()
        curses.curs_set(1) 
    
    return score


def main():
    code = read_input()
    print(part1(code))
    print(part2(code, True))

if __name__ == "__main__":
    main()
