#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
make_loaddata.py

Convert ken_all.csv to loaddata
"""
import argparse
import csv


def merge_separated_line(args):
    """
    yields line

    yields a line.
    if two (or more) lines has same postalcode,
    merge them.
    """

    def is_dup(line, buff):
        """ lines is duplicated or not """
        # same postalcode
        if line[2] != buff[2]:
            return False
        # include choume and not
        if line[11] != buff[11]:
            return False
        # line contains touten(kana)
        if line[5].count(u'、') != 0:
            return True
        if buff[5].count(u'、') != 0:
            return True
        # line contains touten(kanji)
        if line[8].count(u'、') != 0:
            return True
        if buff[8].count(u'、') != 0:
            return True
        return False

    def merge(line, buff):
        """ merge address of two lines """
        new_buff = []
        idx = 0
        for element in line:
            if element[:len(buff[idx])] != buff[idx]:
                new_buff.append(u''.join([buff[idx], element]))
            else:
                new_buff.append(buff[idx])
            idx += 1
        return new_buff

    line_buffer = []
    ken_all = csv.reader(open(args.source))
    for line in ken_all:
        unicode_line = [unicode(s, 'utf8') for s in line]
        if not(line_buffer):
            line_buffer = unicode_line
            continue
        if is_dup(unicode_line, line_buffer):
            line_buffer = merge(unicode_line, line_buffer)
        else:
            yield line_buffer
            line_buffer = unicode_line
    yield line_buffer

def parse_args():
    # parse aruguments
    Parser = argparse.ArgumentParser(description='Make loaddata of postalcode.')
    Parser.add_argument('source', help='input file of converting')
    Parser.add_argument('area', help='data file for area-code')
    Parser.add_argument('net', help='data file of net-code')
    return Parser.parse_args()

def main(args):
    # converting main
    Areadata = csv.writer(open(args.area, 'w'),
                          delimiter=',',
                          quoting=csv.QUOTE_NONE)
    Netdata = csv.writer(open(args.net, 'w'),
                         delimiter=',',
                         quoting=csv.QUOTE_NONE)
    for line in merge_separated_line(args):
        zipcode = line[2]
        if zipcode[5:7] != '00':
            Areadata.writerow([s.encode('utf8') for s in line])
        else:
            Netdata.writerow([s.encode('utf8') for s in line])

if __name__ == '__main__':
    args = parse_args()
    main(args)

