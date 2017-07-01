# coding: utf-8
__author__ = "HanQian"

class A:

    def g(self):
        return "ggg"

class B(A):

    def __init__(self):
        self.f = super(B,self).g()

e = B()
print(e.f)
