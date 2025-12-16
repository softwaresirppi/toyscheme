from itertools import *
from functools import *
from operator import *
from math import *
from utilities import *

def satisfies(f):
    def parse(text):
        if text and f(text[0]):
            return text[0], text[1:]
        else:
            raise SyntaxError(f"Cant Parse: {text}")
    return parse

def sequence(*patterns):
    def parser(text):
        rest = text
        things = []
        for pattern in patterns:
            thing, rest = pattern(rest)
            if thing != None:
                things.append(thing)
        return things, rest
    return parser

def alternate(*patterns):
    def parser(text):
        for pattern in patterns:
            try:
                thing, rest = pattern(text)
                return thing, rest
            except SyntaxError:
                pass
        raise SyntaxError('None of the alternations satisfied')
    return parser

def zeroOrMany(pattern):
    def parser(text):
        rest = text
        things = []
        while True:
            try:
                thing, rest = pattern(rest)
            except SyntaxError:
                return things, rest
            things.append(thing)
    return parser

def apply(f, pattern):
    def parser(text):
        thing, rest = pattern(text)
        return f(thing), rest
    return parser

def complete(pattern):
    def parser(text):
        thing, rest = pattern(text)
        if rest:
            raise SyntaxError(f"Unconsumed Input: {rest}")
        else:
            return thing, ''
    return parser

def thing_of(pattern):
    def f(text):
        thing, rest = pattern(text)
        return thing
    return f

def rest_of(pattern):
    def f(text):
        thing, rest = pattern(text)
        return rest
    return f

def nothing(text):
    return (None, text)
def universe(text):
    raise SyntaxError('Not Whole Universe')
tag = lambda x: lambda text: (x, text)

optional = lambda pattern: alternate(pattern, nothing)
ignored = lambda pattern: apply(lambda matched: None, pattern)
flat = lambda pattern: apply(flatten, pattern)
oneOrMany = lambda pattern: flat(sequence(pattern, zeroOrMany(pattern)))
deep_flat = lambda pattern: apply(lambda x: fixed_point(flatten, x), pattern)
deep_string = lambda pattern: apply(lambda matched: ''.join(map(str, fixed_point(flatten, matched))), pattern)

space = satisfies(lambda x: x.isspace())
alphabet = satisfies(lambda x: x.isalpha())
lower = satisfies(lambda x: x.islower())
upper = satisfies(lambda x: x.isupper())
digit = satisfies(lambda x: x.isdigit())
character = lambda c: satisfies(lambda x: x == c)
string = lambda s: deep_string(sequence(*[character(c) for c in s]))
spacious = lambda pattern: flat(sequence(ignored(zeroOrMany(space)), pattern, ignored(zeroOrMany(space))))

def number(text):
    return apply(lambda x: int(floor(float(x))) if floor(float(x)) == float(x) else float(x), deep_string(
            sequence(
                    alternate(character('-'), character('+'), nothing),
                    alternate(
                        sequence(oneOrMany(digit), character('.'), zeroOrMany(digit)),
                        oneOrMany(digit)))))(text)

def integer(text):
    return apply(int, deep_string(
            sequence(
                alternate(character('-'), character('+'), nothing),
                oneOrMany(digit))))(text)