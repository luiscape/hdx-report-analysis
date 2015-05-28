#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from activity_collect import collect

#
# Running program.
#
def Main():
  '''Main program function.'''

  collect.CollectPackageActivityData(limit=50000)
  collect.CollectCountryActivityData()

if __name__ == '__main__':
  Main()