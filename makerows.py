#! -*- coding:utf8 -*-

import sys
from time import time,sleep,strftime
from random import randint

def write(file, text):
    with open(file, 'a', encoding='utf8') as f:
        print(text)
        f.write(text+'\n')


def main():
    try:
        logfile = sys.argv[1]
    except IndexError:
        logfile = 'nodes.log'

    nodes = {}
    run = True
    while(run):
        sleep(randint(0,3))
        row = strftime("%Y-%m-%d %H:%M:%S")
        node = str(randint(302,310))
        try:
            value = nodes[node]
        except KeyError:
            value = randint(20,80)
        if value < 20:
            value += randint(0,10)
        elif value >= 20 and value < 80:
            value += randint(-10, 10)
        else:
            value -= randint(0,10)
        nodes[node] = value

        row += " Node "+str(node)+" usage is "+str(value) 
        write(logfile, row)

if __name__ == '__main__':
    main()

