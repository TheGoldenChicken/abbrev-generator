#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 22:47:25 2021

@author: dayman
"""

import argparse
from math import sqrt

# Create parser
parser = argparse.ArgumentParser(description = 'Testing argparse')

parser.add_argument('--thing', type=float, default = 4,
                    help = 'Get the square root of stuff')
parser.add_argument('--list', nargs=4)
parser.add_argument('-v', '--verbosity', action='count',
                    help = 'Increase verbosity')

#parser.add_argument('prin', type=str)

# Get all arguments from parser
args = parser.parse_args()

ls = args.list


print(args.thing)
if args.verbosity == 1:
    print('yas')

