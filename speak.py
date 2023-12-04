"""
A script which transforms Python code into a
formally defined subset of English appropriate for
being spoken aloud by humans or TTS engines.
Inspired by MathSpeak: https://www.seewritehear.com/accessible-mathml/mathspeak/

TODO: Determine how to say nesting
TODO: Determine how to retrieve comments
"""

import ast
from itertools import chain


def unshift(it, value):
    yield value
    yield from it

def to_python_speak(node) -> str:
    match node:
        # Root nodes
        case ast.Module(body, _) | ast.Interactive(body):
            # Figure out docstrings
            return "\n\n".join(map(to_python_speak, body))
        case ast.Expression(body):
            return to_python_speak(body)
        case ast.FunctionType():
            raise TypeError('node type FunctionType not supported')
        # Literals
        case ast.Constant(value):
            return to_python_speak(value)
        case int() | None:
            return str(value)
        case str():
            return f'StartString {value.strip()} EndString'
        case tuple():
            return f'StartTuple {" comma ".join(map(value, to_python_speak))} EndTuple'
        case frozenset():
            return f'StartSet {" comma ".join(map(value, to_python_speak))} EndSet'
        # TODO: supporting this looks like its going to be quite complicated
        # case ast.FormattedValue(value, conversion, format_spec):
        #     return
        case ast.List(elts, _):
            return f'StartList {" comma ".join(map(elts, to_python_speak))} EndList'
        case ast.List(elts, _):
            return f'StartTuple {" comma ".join(map(elts, to_python_speak))} EndTuple'
        case ast.Set(elts, _):
            return f'StartSet {" comma ".join(map(elts, to_python_speak))} EndSet'
        case ast.Dict(keys, values):
            return f'StartDict {" comma ".join(f"key {key} value {value}" for key, value in zip(keys, values))} EndDict'
        # Variables
        case ast.Name(id, _):
            return id
        case ast.Starred(id, _):
            return f"Star {id}"
        # Expressions
        case ast.Expr(value):
            return to_python_speak(value)
        case ast.UnaryOp(op, operand):
            return f"{to_python_speak(op)} {to_python_speak(operand)}"
        case ast.UAdd():
            return "positive"
        case ast.USub():
            return "negative"
        case ast.Not():
            return "not"
        case ast.Invert():
            return "bitwise not"
        case ast.BinOp(left, op, right):                
            return f"{to_python_speak(left)} {to_python_speak(op)} {to_python_speak(right)}"
        case ast.Add():
            return "plus"
        case ast.Sub():
            return "minus"
        case ast.Mult():
            return "times"
        case ast.Div():
            return "div"
        case ast.FloorDiv():
            return "floor div"
        case ast.Mod():
            return "mod"
        case ast.Pow():
            return "pow"
        case ast.LShift():
            return "left shift"
        case ast.RShift():
            return "right shift"
        case ast.BitOr():
            return "bitwise or"
        case ast.BitXor():
            return "bitwise ex-or"
        case ast.BitAnd():
            return "bitwise and"
        case ast.MatMult():
            return "mat mul"
        case ast.BoolOp(op, values):
            return f" {to_python_speak(op)} ".join(map(to_python_speak, values))
        case ast.And():
            return "and"
        case ast.Or():
            return "or"
        case ast.Compare(left, ops, comparators):
            " ".join(
                map(
                    to_python_speak,
                    unshift(
                        chain.from_iterable(zip(ops, comparators)),
                        left
                    )
                )
            )
        case ast.Eq():
            return "equal to"
        case ast.NotEq():
            return "not equal to"
        case ast.Lt():
            return "less than"
        case ast.LtE():
            return "less than or equal to"
        case ast.Gt():
            return "greater than"
        case ast.GtE():
            return "greater than or equal to"
        case ast.Is():
            return "is"
        case ast.IsNot():
            return "is not"
        case ast.In():
            return "in"
        case ast.NotIn():
            return "not in"
        case _:
            raise NotImplementedError(ast.dump(node) if isinstance(node, ast.AST) else node)

def python_speak(*args, **kwargs) -> str:
    tree = ast.parse(*args, **kwargs)
    return to_python_speak(tree)

if __name__ == '__main__':
    from sys import argv
    with open(argv[1]) as f:
        print(python_speak(f.read(), f.name))
