#!/usr/bin/env python

#include <stdiom.h>
from time import time
from math import *
from random import randint
from sys import argv, setrecursionlimit
from signal import signal, SIGINT
from argparse import ArgumentParser

from parsing_combinators import *
from utilities import *
from toyscheme_objects import *
from operator import *
from decimal import Decimal, getcontext
from picture import open_picture, draw_line, close_picture
from music import begin_music, play_sine_wave, end_music
# Interpreter TODO
# someway to neatly handle the conversion of scheme objects in python interface functions
# make music realtime
# music cache the waves and extend it if a larger wave needed
# bang! all destructive functions
# primitives and macros used as funcitons
# DONT LET THE PROGRAMMER REDEFINE.
# load a file once
# Maybe move to plain floats?
# implement genric polymorphism of some sort (like haskell disjoint functions)
# Remove or keep pow operator? Print rationals as rationals or floats?
# introduce infinity, infinitesimal, other special values
# make sure macros can be called like functions
# proper cons equality
# [SYNTAX-SUGAR] Try implementing arbitrary input function (lambda x x)
# [AESTHETICS] Rewrite trace logic
# [COMPLIANCY] else in cond last expression
# [SYNTAX-SUGAR] implement let*, letrec
# [AESTHETICS] detect cycles when printing cons chains
# implement eval apply
# an APL-ish unified interface for lists, sets, maps, image, audio, etc...
# make input function read like the interpreter prompt

# ToyScheme TODO
# understanding linear algebra (vectors and matrices)
# Implement BST
# map, filter and fold for other dimensions? what about accumulate-n?
# implement taylor series, logs, etc
# Interval problem: Handling Depended or Synchronized values.
# Prove fib(x) = phi^x / sqrt(5)
# Rabin Miller Test? Cant be Fooled?
# automated random input testing
# rubix cube solving algo
# combinations and permutations

# REVOLUTIONARY 
# clean and simple macro system
# cleaner quasiquoting list with []
# only rationals?

# PRIMITIVES
# SYNTAX: let* define* if* cond* quote* begin
# FUNCTIONS: lambda? lambda* (f x)* TODO eval apply
# PAIRS: nil? cons? nil cons car cdr TODO list
# NUMBERS: number? zero? incr decr + - * / < <= > >= =
# BOOLEANS: and* or* not
# SYMBOLS: eq?

# DIFFERENCES
# empty cond returns nil
# define returns the value thats being defined
# UPPER CASE is a symbol everything else is lookedup
# it refers to previous top level expression's result

class Scheme:
    def __init__(self, traceLevel, quiet):
        self.traceLevel=traceLevel
        self.quiet = quiet
        self.loaded = []
        self.globals = {}
        def scheme_error(message):
            raise ValueError(message)
        self.primitives = {
            # System stuff
            'input': SchemePrimitive(lambda : input('> ')),
            'print': SchemePrimitive(lambda arg: (lambda _: arg)(print(arg, end=''))),
            'newline': SchemePrimitive(lambda: (lambda _: schemeNil)(print())),
            'error': SchemePrimitive(scheme_error),
            'random': SchemePrimitive(lambda n: SchemeNumber(randint(0, int(n) - 1))),
            'time': SchemePrimitive(lambda : time()),

            # Nil and Symbols
            'symbol?': SchemePrimitive(lambda x: SchemeBoolean(isinstance(x, str))),
            'eq?': SchemePrimitive(lambda x, y: SchemeBoolean(x is y)),
            'nil?' : SchemePrimitive(lambda x: SchemeBoolean(isinstance(x, SchemeNil))),
            'nil': schemeNil,

            # Functions
            'lambda?': SchemePrimitive(lambda x: SchemeBoolean(isinstance(x, SchemeLambda))),

            # Pairs
            'cons?': SchemePrimitive(lambda x: SchemeBoolean(isinstance(x, SchemeCons))),
            'cons': SchemePrimitive(lambda x, y: SchemeCons(x, y)),
            'car': SchemePrimitive(lambda x: x.car),
            'cdr': SchemePrimitive(lambda x: x.cdr),

            # BOOLEANS
            'boolean?': SchemePrimitive(lambda x: SchemeBoolean(isinstance(x, SchemeBoolean))),
            'true': schemeTrue,
            'false': schemeFalse,
            'not': SchemePrimitive(lambda x: SchemeBoolean(x == schemeFalse)),

            # Numbers
            'number?': SchemePrimitive(lambda x: SchemeBoolean(isinstance(x, SchemeNumber))),
            'zero?': SchemePrimitive(lambda x: SchemeBoolean(x == schemeZero)),
            'incr': SchemePrimitive(lambda x: x + schemeOne),
            'decr': SchemePrimitive(lambda x: x - schemeOne),
            'floor': SchemePrimitive(floor),
            'round': SchemePrimitive(round),
            'ceil': SchemePrimitive(ceil),
            'mod': SchemePrimitive(mod),
            '+': SchemePrimitive(add),
            '*': SchemePrimitive(mul),
            '-': SchemePrimitive(sub),
            '/': SchemePrimitive(truediv),
            '^': SchemePrimitive(pow), # kinda cheating
            '<': SchemePrimitive(lambda x, y: SchemeBoolean(x < y)),
            '<=': SchemePrimitive(lambda x, y: SchemeBoolean(x <= y)),
            '>=': SchemePrimitive(lambda x, y: SchemeBoolean(x >= y)),
            '>': SchemePrimitive(lambda x, y: SchemeBoolean(x > y)),
            '=': SchemePrimitive(lambda x, y: SchemeBoolean(x == y)),
            '!=': SchemePrimitive(lambda x, y: SchemeBoolean(x != y)),

            # Picture
            'open-picture': SchemePrimitive(open_picture),
            'draw-line': SchemePrimitive(draw_line),
            'close-picture': SchemePrimitive(close_picture),

            # Music
            'begin-music!': SchemePrimitive(begin_music),
            'play-sine-wave!': SchemePrimitive(play_sine_wave),
            'end-music!': SchemePrimitive(end_music),
        }
        def ctrlc(signum, frame):
            print('Tata!')
            exit(0)
        setrecursionlimit(2048) 
        signal(SIGINT, ctrlc)

    @staticmethod
    def main(argv):
        parser = ArgumentParser(description='Toy Scheme Implementation')
        parser.add_argument('--trace', '-t', type=int, default=0, help='Trace levels are none(0), functions(1), all(2), all with bindings(3)')
        parser.add_argument('--interactive', '-i', action='store_true', help='Force interactive mode after running files')
        parser.add_argument('--quiet', '-q', action='store_true', help='Suppress welcome and loaded messages')
        parser.add_argument('--precision', '-p', type=int, default=4, help='How precise the numbers have to be') 
        parser.add_argument('files', nargs='*', help='Scheme files to interpret')  # Positional argument
        args = parser.parse_args(argv)
        getcontext().prec = args.precision
        scheme = Scheme(args.trace, args.quiet)
        if args.files:
            scheme.evaluate({}, ['load', *args.files])
            if args.interactive:
                scheme.repl()
        else:
            if not args.quiet:
                print('This is Toy Scheme. You got lambdas, pairs, numbers, booleans, symbols and nil. Play around.')
            scheme.repl()

    def stripComments(interpreter, code):
        return '\n'.join([line.split(';', 1)[0] for line in code.split('\n')])
    
    def parse(interpreter, text):
        def symbol(text):
            return deep_string(
                alternate(
                    sequence(
                        ignored(character("'")),
                        oneOrMany(satisfies(lambda x: x not in "[](){}'")),
                        ignored(character("'"))
                    ),
                    oneOrMany(satisfies(lambda x: x not in '[](){}' and not x.isspace())))
                )(text)

        def number(text):
            return apply(SchemeNumber, deep_string(
                    sequence(
                            alternate(character('-'), character('+'), nothing),
                            alternate(
                                sequence(oneOrMany(digit), character('.'), zeroOrMany(digit)),
                                oneOrMany(digit),
                                string('infinity')
                                ))))(text)
        
        def sexp(text):
            return spacious(alternate(
                    flat(sequence(
                        tag('list'),
                        ignored(character('[')),
                        zeroOrMany(sexp),
                        ignored(character(']')))),
                    flat(sequence(
                        tag('quote'),
                        ignored(character('\'')),
                        sequence(sexp))),
                    flat(sequence(
                        ignored(character('(')),
                        zeroOrMany(sexp),
                        ignored(character(')')))),
                    number,
                    symbol))(text)
        return thing_of(complete(zeroOrMany(sexp)))(text)
    
    @staticmethod
    def preserve_last_expression(evaluator):
        def preserved_evaluator(interpreter, locals, ast, topLevel=False):
            result = evaluator(interpreter, locals, ast, topLevel)
            if topLevel:
                interpreter.globals['it'] = result
            return result
        return preserved_evaluator

    @staticmethod
    def trace(evaluator):
        def traced_evaluator(interpreter, locals, ast, topLevel=False):
            if interpreter.traceLevel == 0:
                return evaluator(interpreter, locals, ast, topLevel)
            else:
                if not hasattr(traced_evaluator, 'depth'):
                    traced_evaluator.depth = 0
                traced_evaluator.depth += 1
                if interpreter.traceLevel == 1:
                    if isinstance(ast, list):
                        print(f"{'║ ' * (traced_evaluator.depth - 1)}╔═ {ast}")
                        result = evaluator(interpreter, locals, ast, topLevel)
                        print(f"{'║ ' * (traced_evaluator.depth - 1)}╚═ {result}")
                        traced_evaluator.depth -= 1
                        return result
                    else:
                        result = evaluator(interpreter, locals, ast, topLevel)
                        traced_evaluator.depth -= 1
                        return result
                elif interpreter.traceLevel == 2:
                    print(f"{'║ ' * (traced_evaluator.depth - 1)}╔═ {ast}")
                    result = evaluator(interpreter, locals, ast, topLevel)
                    print(f"{'║ ' * (traced_evaluator.depth - 1)}╚═ {result}")
                    traced_evaluator.depth -= 1
                    return result
                elif interpreter.traceLevel == 3:
                    print(f"{'║ ' * (traced_evaluator.depth - 1)}╔═ {ast}", f"locals: {locals} globals: {interpreter.globals}")
                    result = evaluator(interpreter, locals, ast, topLevel)
                    print(f"{'║ ' * (traced_evaluator.depth - 1)}╚═ {result}")
                    traced_evaluator.depth -= 1
                    return result
        return traced_evaluator

    @trace
    @preserve_last_expression
    def evaluate(interpreter, locals, ast, topLevel=False):
        match ast:
            case number if isinstance(number, SchemeNumber):
                return number
            case symbol if isinstance(symbol, str): 
                if symbol.isupper():
                    return symbol
                elif symbol in interpreter.primitives:
                    return interpreter.primitives[symbol]
                elif symbol in locals:
                    return locals[symbol]
                elif symbol in interpreter.globals:
                    return interpreter.globals[symbol]
                else:
                    raise SyntaxError(f'Unbound: {symbol}')
            case ['load', *files]:
                for file in files:
                    if file not in interpreter.loaded:
                        interpreter.loaded += [file]
                        with open(file, 'r', encoding='utf-8') as f:
                            if not interpreter.quiet:
                                print(f'Loaded {file}')
                            interpreter.interpret(f.read())
                        return schemeNil
                return schemeNil
            case ['and', *args]:
                actual_arg = schemeTrue
                for arg in args:
                    actual_arg = interpreter.evaluate(locals, arg)
                    if actual_arg == schemeFalse:
                        return schemeFalse
                return actual_arg
            case ['or', *args]:
                for arg in args:
                    actual_arg = interpreter.evaluate(locals, arg)
                    if actual_arg != schemeFalse:
                        return actual_arg
                return schemeFalse
            case ['quote', x]:
                def quote(ast):
                    match ast:
                        case []: return schemeNil
                        case [first, *rest]: return SchemeCons(quote(first), quote(rest))
                        case something: return something
                return quote(x)
            case ['list', *xs]:
                def consify(xs):
                    match xs:
                        case []: return schemeNil
                        case [first, *rest]: return SchemeCons(interpreter.evaluate(locals, first), consify(rest))
                        case something: return something
                return consify(xs)                
            case ['if', test, true_expr, false_expr]:
                if interpreter.evaluate(locals, test) != schemeFalse:
                    return interpreter.evaluate(locals, true_expr)
                else:
                    return interpreter.evaluate(locals, false_expr)
            case ['begin', *expressions]:
                last = schemeNil
                for expression in expressions:
                    last = interpreter.evaluate(locals, expression, topLevel=topLevel)
                return last
            case ['cond', *clauses]:
                for test, *expr in clauses:
                    if interpreter.evaluate(locals, test):
                        return interpreter.evaluate(locals, ['begin', *expr])
                return schemeNil
            case ['let', [*name_values], *body]:
                return interpreter.evaluate(locals | dict([(name, interpreter.evaluate(locals, value)) for name, value in name_values]), ['begin', *body])
            case ['lambda', [*wildcards], *body]: return SchemeLambda(locals, wildcards, (), ['begin', *body]) # locals, wildcards, values, body
            case ['define', [function_name, *wildcards], *body]:
                (interpreter.globals if topLevel else locals)[function_name] = SchemeLambda(locals, wildcards, (), ['begin', *body])
                return SchemeLambda(locals, wildcards, (), ['begin', *body])
            case ['define', name, value]:
                evaluated_value = interpreter.evaluate(locals, value)
                (interpreter.globals if topLevel else locals)[name] = evaluated_value
                return evaluated_value
            case [fn, *args]:
                actual_fn = interpreter.evaluate(locals, fn)
                actual_args = [interpreter.evaluate(locals, arg) for arg in args]
                if isinstance(actual_fn, SchemeFunction):
                    return actual_fn(interpreter, *actual_args)
                else:
                    raise SyntaxError(f"Cant apply something thats not a function")
        raise SyntaxError(f'Unknown Expression: {ast}')
    
    def interpret(interpreter, code):
        try:
            return pipe(code, 
                interpreter.stripComments,
                interpreter.parse,
                lambda x: ['begin', *x],
                partial(interpreter.evaluate, {}, topLevel=True))
        except Exception as e:
            # raise e
            print(f"\033[31m{e}\033[0m")
            return schemeNil

    def repl(interpreter):
        result = interpreter.interpret(input("\033[33mλ \033[0m"))
        if result != schemeNil:
            print(result)
        interpreter.repl()

if __name__ == '__main__':
    Scheme.main(argv[1:])