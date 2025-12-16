from inspect import signature, Parameter
from math import floor, ceil
from functools import partial
from decimal import Decimal, getcontext

class SchemeFunction:
    def __call__(self, interpreter, *args):
        raise NotImplementedError()
    def arity(self):
        raise NotImplementedError()

class SchemeLambda(SchemeFunction):
    def __init__(self, locals, wildcards, values, body):
        if not isinstance(wildcards, list):
            raise Exception("wildcards should be a list")
        self.wildcards = wildcards
        self.values = values
        self.body = body
        self.locals = locals    
    def arity(self):
        return len(self.wildcards) - len(self.values)
    def __call__(self, interpreter, *args):
        if len(args) < self.arity(): # curry
            return SchemeLambda(self.locals, self.wildcards, self.values + args, self.body)
        if self.arity() < len(args): # re-apply
            exact_arguments = args[:self.arity()]
            excess_arguments = args[self.arity():]
            return self(interpreter, *exact_arguments)(interpreter, *excess_arguments)
        return interpreter.evaluate(self.locals | dict(zip(self.wildcards, self.values + args)), self.body)
    def __repr__(self):
        return f'#<{self.arity()}-ary lambda>'

class SchemePrimitive(SchemeFunction):
    def __init__(self, f):
        self.f = f
    
    def arity(self):
        for param in signature(self.f).parameters.values():
            if param.kind == Parameter.VAR_POSITIONAL or param.kind == Parameter.VAR_KEYWORD:
                return float('inf')
        return len(signature(self.f).parameters.values())
    
    def __call__(self, interpreter, *args):
        if len(args) < self.arity(): # curry
            return SchemePrimitive(partial(self.f, *args))
        if self.arity() < len(args): # re-apply
            exact_arguments = args[:self.arity()]
            excess_arguments = args[self.arity():]
            return self(interpreter, *exact_arguments)(interpreter, *excess_arguments)
        return self.f(*args)
    def __repr__(self):
        return '#<primitive>'

class SchemeCons:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr
    def __eq__(self, other):
        if isinstance(other, SchemeCons):
            return self.car == other.car and self.cdr == other.cdr
        return False
    def __repr__(self):
        def proper_list(x):
            match x:
                case SchemeNil(): return []
                case SchemeCons(): return [x.car] + proper_list(x.cdr)
                case something_else: raise ValueError('Not a proper list')
        try:
            return f"[{' '.join(map(str, proper_list(self)))}]"
        except ValueError:
            return f"({self.car} . {self.cdr})"

class SchemeNil:
    def __repr__(self):
        return 'nil'
    def __eq__(self, value):
        return isinstance(value, SchemeNil)

class SchemeBoolean:
    def __init__(self, x):
        if isinstance(x, SchemeBoolean):
            self.state = x.state
        elif x:
            self.state = True
        else:
            self.state = False
    
    def __eq__(self, other):
        if isinstance(other, SchemeBoolean):
            return self.state == other.state
        return False

    def __bool__(self):
        return self.state

    def __repr__(self):
        if self.state:
            return 'true'
        else:
            return 'false'

class SchemeNumber:
    def __init__(self, value):
        self.value = Decimal(value) + 0
    
    def __float__(self):
        return float(self.value)

    def __eq__(self, other):
        if isinstance(other, SchemeNumber):
            return self.value == other.value
        return False
    
    def __ne__(self, other):
        if isinstance(other, SchemeNumber):
            return self.value != other.value
        return True
    
    def __lt__(self, other):
        return self.value < other.value
    def __le__(self, other):
        return self.value <= other.value
    def __gt__(self, other):
        return self.value > other.value
    def __ge__(self, other):
        return self <= other
    
    def __floor__(self):
        return SchemeNumber(floor(self.value))
    def __ceil__(self):
        return SchemeNumber(ceil(self.value))
    def __mod__(a, b):
        return SchemeNumber(a.value % b.value)
    def __add__(a, b):
        return SchemeNumber(a.value + b.value)
    def __neg__(self):
        return SchemeNumber(-self.value)
    def __sub__(a, b):
        return SchemeNumber(a.value - b.value)
    def __mul__(a, b):
        return SchemeNumber(a.value * b.value)
    def __truediv__(a, b):
        return SchemeNumber(a.value / b.value)
    def __pow__(a, b):
        return SchemeNumber(a.value ** b.value)
    def __int__(self):
        return floor(self.value)
    def __repr__(self):
        return str(self.value)

schemeNil = SchemeNil()
schemeZero = SchemeNumber(0)
schemeOne = SchemeNumber(1)
schemeTrue = SchemeBoolean(True)
schemeFalse = SchemeBoolean(False)
