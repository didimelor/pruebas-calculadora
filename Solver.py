import sympy as sym
from sympy import *
import time
import numpy as np
from sympy.parsing.mathematica import mathematica

x = sym.Symbol('x')
usrInput = "x**3"
expr = x**2
exprD = 2*x


def parse(usrInput):
    global expr
    usrInput = usrInput.replace("\\", "/")
    if(usrInput.find("Log" or "log") != -1):
        mathematica(usrInput)
    expr = parse_expr(usrInput)
    expr = simplify(expr)

def f(var):
    return expr.subs(x, var)

def df(x,f):
    h = .00001
    upper = f(x+h)
    lower = f(x)
    return (upper - lower) / h
class function:
    def __init__(self, id, sol, it, t, acc, solved, message):
        self.id = id
        self.sol = sol
        self.it = it
        self.t = t
        self.acc = acc
        self.solved = solved #bool if solved
        self.message = message

def Solver11(x0,f):
    it = 0
    maxIt = 100
    start = time.time()
    x_n  = x0
    x_n_1 = x_n + .01
    step = x_n_1-x_n
    while (abs(step) > 0.00001 and it < maxIt):
        it += 1
        denominator = df(x_n,f)
        if denominator != 0:
            function_result = f(x_n) 
            x_n_1 = x_n - function_result / denominator
        else:
            x_n = 0.0
            return function(usrInput, x_n, it, (round(time.time() - start,12)), 0.0, 0, "No solution found")

        step = x_n_1-x_n
        x_n = x_n_1
    if(it > maxIt):
        x_n = 0.0
        return function(usrInput, x_n, it, (round(time.time() - start,12)), 0.0, 0, "No solution found")
    return function(usrInput, (round(x_n,12)), it, (round(time.time() - start,12)), 0.001, 1, "Solved!")

'''
parse("3*(x)*(x)+4*(x)-10")
funcObj = Solver11(0.2,f)
print(funcObj.sol, funcObj.message)
'''

