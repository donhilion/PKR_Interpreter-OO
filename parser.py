from functools import reduce
from re import VERBOSE
from distorm3 import _Value
from funcparserlib.lexer import make_tokenizer, Token
from funcparserlib.parser import some, a, skip, with_forward_decls, many, maybe

__author__ = 'Donhilion'

UNDEFINED = None

# leaves of the AST
class Exp(object):

    def eval(self, env):
        return UNDEFINED

class Const(Exp):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Constant(%s)" % self.value

class Variable(Exp):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Variable(%s)" % self.name

class Assignment(Exp):

    def __init__(self, variable, exp):
        self.variable = variable
        self.exp = exp

    def __str__(self):
        return "Assignment(%s, %s)" % (self.variable, self.exp)

class Declaration(Exp):

    def __init__(self, variable, exp):
        self.variable = variable
        self.exp = exp

    def __str__(self):
        return "Declaration(%s, %s)" % (self.variable, self.exp)

class IfThenElse(Exp):

    def __init__(self, cond, then, els=None):
        self.cond = cond
        self.then = then
        self.els = els

    def __str__(self):
        return "If(%s, %s, %s)" % (self.cond, self.then, self.els)

class While(Exp):

    def __init__(self, cond, do):
        self.cond = cond
        self.do = do

    def __str__(self):
        return "While(%s, %s)" % (self.cond, self.do)

class CmdList(Exp):

    def __init__(self, lst):
        self.lst = lst

    def __str__(self):
        string = ""
        for cmd in self.lst:
            string += "%s, " % cmd
        return "CmdList(%s)" % string[:-2]

class Print(Exp):

    def __init__(self, exp):
        self.exp = exp

    def __str__(self):
        return "Print(%s)" % self.exp

class Add(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "Add(%s, %s)" % (self.left, self.right)

class Sub(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "Sub(%s, %s)" % (self.left, self.right)

class Mul(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "Mul(%s, %s)" % (self.left, self.right)

class Div(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "Div(%s, %s)" % (self.left, self.right)

class Eq(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "Eq(%s, %s)" % (self.left, self.right)

class Lt(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "Lt(%s, %s)" % (self.left, self.right)

class Gt(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "Gt(%s, %s)" % (self.left, self.right)


def tokenize(string):
    """
    Generates a list of tokens from the given string.
    """
    specs = [
        ('Op',          (r'[\-+/*=<>]',)),
        ('Assign',      (r':=',)),
        ('Ident', 		(r'[A-Za-z][A-Za-z_0-9]*',)),
        ('Number',      (r'(0|([1-9][0-9]*))', VERBOSE)),
        ('Semicolon',	(';',)),
        ('Lb',          ('{',)),
        ('Rb',          ('}',)),
        ('Lp',          ('(',)),
        ('Rp',          (')',)),
        ]
    useless = ['Space']
    t = make_tokenizer(specs)
    return [x for x in t(str) if x.type not in useless]

def parse(seq):
    """
    Parses the list of tokens and generates an AST.
    """
    def eval_expr(z, list):
        return reduce(lambda s, (f, x): f(s, x), list, z)
    unarg = lambda f: lambda x: f(*x)
    tokval = lambda x: x.value # returns the value of a token
    toktype = lambda t: some(lambda x: x.type == t) >> tokval # checks type of token
    const = lambda x: lambda _: x # like ^^^ in Scala
    eval_cond = lambda x: x[1](x[0], x[2])

    op = lambda s: a(Token('Op', s)) >> tokval # return the value if token is Op
    op_ = lambda s: skip(op(s)) # checks if token is Op and ignores it

    lst = lambda x: [x[0],] + x[1]
    tup = lambda x: (x[0], x[1])

    makeop = lambda s, f: op(s) >> const(f)

    add = makeop('+', Add)
    sub = makeop('-', Sub)
    mul = makeop('*', Mul)
    div = makeop('/', Div)

    lt = makeop('<', Lt)
    gt = makeop('>', Gt)
    eq = makeop('=', Eq)

    point_op = mul | div
    line_op = add | sub
    comp_op = lt | gt | eq

    assign = with_forward_decls(lambda: toktype('Ident') + skip(toktype('Assign')) + exp >> unarg(Assignment))
    ifexp = with_forward_decls(lambda: skip(Token('Ident', "if")) + cond + cmd + \
                                       maybe(skip(Token("Ident", "else")) + cmd) >> unarg(IfThenElse))
    whileexp = with_forward_decls(lambda: skip(Token("Ident", "while")) + cond + cmd >> unarg(While))
    printexp = with_forward_decls(lambda: skip(Token("Ident", "print")) + exp >> unarg(Print))
    vardef = with_forward_decls(lambda: skip(Token("Ident", "var")) + toktype("Ident") + op_("=") + exp \
                                        >> unarg(Declaration))

    cmd = with_forward_decls(lambda: assign | ifexp | whileexp | printexp | vardef | \
                                        skip(toktype('Lb')) + cmd_list + skip(toktype("Rb")))
    cmd_list = (cmd + many(skip(toktype("Semicolon")) + cmd) >> lst) >> unarg(CmdList)

    variable = toktype("Ident") >> unarg(Variable)
    constexp = toktype("Number") >> unarg(Const)
    factor = with_forward_decls(lambda: variable | constexp | \
                                        skip(toktype("Lp")) + exp + skip(toktype("Rp")))
    summand = factor + maybe(point_op + factor) >> unarg(eval_expr)
    exp = summand + maybe(line_op + summand) >> unarg(eval_expr)

    cond = exp + comp_op + exp >> eval_cond

    return cmd.parse(seq)
