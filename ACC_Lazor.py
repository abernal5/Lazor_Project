# -*- coding: utf-8 -*-
"""
EN.640.635 Software Carpentry
Lazor Project


def class Reflect:
    def call(self, lazor):
        if lazor[0] == -1:
            if lazor[1] == 1:
                new_lazor = (1, 1)
            else:
                new_lazor = (1, -1)
        if lazor[1] == 1:
            if lazor[0] == 1:
                new_lazor = (1, -1)
            else:
                new_lazor = (-1,-1)
        return(new_lazor)

def class Opaque:
    def call(self, lazor):
        return(0, 0)


def class Refract:
    def call(self, lazor):
        lazor1 = lazor
        lazor2 = Reflect(lazor)
        return(lazor1, lazor2)
