#!/usr/bin/env python3

import sys
import re
from datetime import date, datetime, time, timedelta

# helper

def is_time_line(l):
    p = re.compile('^[0-9]{2}:')
    m = p.match(l)
    if m is None:
        return False
    else:
      return True


def get_time(s):
    dt = datetime.strptime(s, "%H:%M:%S,%f")
    return dt.time()


def get_str(t):
    return t.strftime("%H:%M:%S,%f")[:-3]


def get_timedelta(h=0, m=0, s=0, mm=0):
    return timedelta(hours=h, minutes=m, seconds=s, microseconds=mm*1000)

def add(t0, delta):
    delta = timedelta(hours=delta.hour,
                     minutes=delta.minute,
                     seconds=delta.second,
                     microseconds=delta.microsecond)
    dt = datetime.combine(date.today(), t0) + delta
    return dt.time()

def sub(t0, delta):
    delta = timedelta(hours=delta.hour,
                     minutes=delta.minute,
                     seconds=delta.second,
                     microseconds=delta.microsecond)
    dt = datetime.combine(date.today(), t0) - delta
    return dt.time()

def get_endpoints(l):
    l = l.rstrip()
    sep = re.compile("[ ]+-->[ ]+")
    ts = sep.split(l)
    return list(map(get_time, ts))


def transform_time_line(l, delta, sens):
    es = get_endpoints(l)
    tes = list()
    for e in es:
      if sens == '+':
        tes.append(add(e, delta))
      else:
        tes.append(sub(e, delta))
    return get_str(tes[0]) + " --> " + get_str(tes[1]) + "\n"

# main

if __name__ == "__main__":

    filesrt = sys.argv[1]
    t0 = get_time(sys.argv[2])
    delta = 0
    sense = ""
    first_time_line = True

    with open("./sample.srt") as inputf:
      print("Reading")
      for l in inputf:
        if is_time_line(l):
          if first_time_line:
            tt0 = get_endpoints(l)[0]
            if tt0 > t0:
              delta = sub(tt0,t0)
              sens = '-'
              print("Delta: -{}".format(get_str(delta)))
            else:
              delta = sub(t0,tt0)
              sens = '+'
              print("Delta: +{}".format(get_str(delta)))
            first_time_line = False
          with open("./sample.srt.new", "a") as outputf:
            outputf.write(transform_time_line(l, delta, sens))
        else:
          with open("./sample.srt.new", "a") as outputf:
            outputf.write(l)
      print("Writing")
