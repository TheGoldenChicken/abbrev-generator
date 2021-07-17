#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 10:58:32 2021

@author: dayman
"""

import argparse
parser = argparse.ArgumentParser(prog='PROG', description='description')
parser.add_argument('--cmd', choices=['create','delete','help','quit'])
parser.add_argument('-v', '--vebos', action='store_true')
parser.add_argument('--list', nargs = '*')


while True:
    astr = input('$: ')
    # print astr
    try:
        args = parser.parse_args(astr.split())
        print(astr.split())
    except SystemExit:
        # trap argparse error message
        print('error')
        continue
    if args.vebos:
        print('It is true')
    
    elif args.cmd in ['create', 'delete']:
        print ('doing', args.cmd)
    elif args.cmd == 'help':
        parser.print_help()
    else:
        print( 'done')
