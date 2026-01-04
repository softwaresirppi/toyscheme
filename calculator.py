#!/usr/bin/env python
from parsing_combinators import *
from signal import signal, SIGINT

# === GRAMMAR ===
# expression = term + expression
# expression = term - expression
# expression = term
# term = factor * term
# term = factor / term
# term = term
# factor = -expr
# factor = number
# factor = (expr)

def factor(text):
    return spacious(
            alternate(
                flat(sequence(ignored(character('(')), expr, ignored(character(')')))), 
                apply(neg, flat(sequence(ignored(character('-')), expr))),
                flat(sequence(ignored(character('+')), expr)),
                number))(text)
    
def term(text):
    return alternate(
                apply(prod, sequence(factor, ignored(character('/')), apply(partial(truediv, 1), term))),
                apply(prod, flat(sequence(factor, ignored(character('*')), term))),
                factor)(text)

def expr(text):
    return alternate(
                apply(sum, flat(sequence(term, ignored(character('+')), expr))),
                apply(sum, flat(sequence(term, ignored(character('-')), apply(neg, expr)))),
                term)(text)

def calculator():
    thing, rest = expr(input('> '))
    match thing, rest:
        case (SyntaxError(msg=message), _):
            print(f"[WTF] {message}")
        case (thing, rest) if rest:
            print(f"[INFO] I only understood before {rest}")
            print(thing)
        case (thing, _): print(thing)
    calculator()

def ctrlc(sig, frame):
    print('Tata!')
    exit(0)

signal(SIGINT, ctrlc)

if __name__ == '__main__':
    print('This is an infix arithmetic calculator.')
    print('You got binary +, -, * and / as well as unary + and - and parens for grouping')
    calculator()