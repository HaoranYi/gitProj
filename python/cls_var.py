#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: t.py
Author: Haoran Yi
Email: hyi@hbk.com
Github: http://github/hyi
Description: Illustrate class variable
"""

class Foo:
    x = [] 
    def __init__(self):
        self.x = Foo.x

f1 = Foo()
print(f1.x)
print(Foo.x)

f2 = Foo()
print(f2.x)
print(Foo.x)


Foo.x.append(1) 
print(f1.x)
print(Foo.x)

print(f2.x)
print(Foo.x)
