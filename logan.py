#! -*- coding:utf8 -*-

import os
import re
import sys
import json
from datetime import datetime,timedelta
from time import time,sleep,strftime,strptime
from random import randint


class Logan:
    def __init__(self, log, threshold=85, interval=10, keep=20):
        # the actual logfile(s)  ! multiple not implemented
        self.log = log
        # data threshold
        self.threshold = threshold
        # time in seconds to read again from the file
        self.interval = interval
        # time in seconds for keep event rows:
        self.keep = keep
        # the file handle for the file for now..
        self.handle = None

    def open(self):
        self.handle = open(self.log,'r')

    def close(self):
        self.handle.close()

    def rows(self):
        if self.handle is None:
            self.open()
        for line in self.handle.read().split("\n"):
            yield line

    def dump(self, data):
        with open('logan.json','w') as f:
            json.dump(data, f, indent=2)

    def show(self, data):
        o = os.system('clear')
        print("Logan, threshold: {}".format(self.threshold))
        print("- - - Node status - - -")
        print("     {:3}   {:3}   {:7}    Eventcount\n".format('id','%','status'))
        for k in data.keys():
            newest = None
            for r in sorted(data[k]['events'], key=lambda k: k['timestamp']):
                newest = r
            print("Node {:3} [ {:3} : {:7} ], {}".format(
                k, newest['value'], data[k]['status'], str(len(data[k]['events'])))
            )
            # strftime("%Y-%m-%d %H:%M:%S",newest['timestamp']))


def main():
    try:
        logfile = sys.argv[1]
    except IndexError:
        logfile = 'nodes.log'
    logan = Logan(logfile, threshold=50)
    
    # nodes to grab
    nodes = {}
    waitcounter = 0
    try:
        while True:
            if waitcounter >= logan.interval:
                # logan.dump(nodes)
                waitcounter = 0
            for row in logan.rows():
                if row != '':
                    # split the row
                    data = row.split()
                    # combine date back
                    tstamp = datetime.strptime(" ".join(data[0:2]),'%Y-%m-%d %H:%M:%S')
                    # grab node name
                    node = None
                    for found in re.findall('Node \d{1,}', row):
                        text, node = found.split()
                    # grab node value
                    value = None
                    for found in re.findall('usage is \d{1,}', row):
                        text, verb, value = found.split()
                    # combine to nodes
                    try:
                        selection = nodes[node]
                    except KeyError:
                        selection = {"status": "Normal", "events": list()}
                    selection['events'].append({
                        "timestamp": tstamp,
                        "value": value
                    })
                    # Check threshold
                    if int(value) > logan.threshold:
                        selection['status'] = 'Problem'
                    else:
                        selection['status'] = 'Normal' 
                    # Actually save
                    nodes[node] = selection

                else:
                    sleep(1)
                    logan.show(nodes)
                    waitcounter += 1


    except KeyboardInterrupt:
        print("\nStopped handling")
        if logan.handle is not None:
            logan.close()


if __name__ == '__main__':
    main()

