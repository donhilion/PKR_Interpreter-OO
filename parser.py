from functools import reduce
from re import VERBOSE
from funcparserlib.lexer import make_tokenizer, Token
from funcparserlib.parser import some, a, skip, with_forward_decls, many, maybe
from ast import Add, Sub, Mul, Div, Lt, Gt, Eq, Or, And, Neq, Not, Le, Ge, Assignment, IfThenElse, While, Print, Declaration, CmdList, Variable, Const
from env import Env

__author__ = 'Donhilion'

def tokenize(string):
    """
    Generates a list of tokens from the given string.
    """
    specs = [
        ('Space',		(r'[ \t\r\n]+',)),
        ('Or',          ('\|\|',)),
        ('And',         ('&&',)),
        ('Neq',         ('!=',)),
        ('Not',         ('!',)),
        ('Eq',          ('==',)),
        ('Assign',      (':=',)),
        ('Le',          ('<=',)),
        ('Ge',          ('>=',)),
        ('Op',          (r'[\-+/*=<>]',)),
        ('Ident', 		(r'[A-Za-z][A-Za-z_0-9]*',)),
        ('Number',      (r'(0|([1-9][0-9]*))', VERBOSE)),
        ('Semicolon',	(';',)),
        ('Lb',          ('{',)),
        ('Rb',          ('}',)),
        ('Lp',          ('\(',)),
        ('Rp',          ('\)',)),
        ]
    useless = ['Space']
    t = make_tokenizer(specs)
    return [x for x in t(string) if x.type not in useless]

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

    ident = lambda s: a(Token('Ident', s)) >> tokval # return the value if token is Op
    ident_ = lambda s: skip(ident(s)) # checks if token is Op and ignores it

    lst = lambda x: [x[0],] + x[1]

    makeop = lambda s, f: op(s) >> const(f)

    add = makeop('+', Add)
    sub = makeop('-', Sub)
    mul = makeop('*', Mul)
    div = makeop('/', Div)

    lt = makeop('<', Lt)
    gt = makeop('>', Gt)
    eq = toktype('Eq') >> const(Eq)
    orop = toktype('Or') >> const(Or)
    andop = toktype('And') >> const(And)
    neq = toktype('Neq') >> const(Neq)
    notop = toktype('Not') >> const(Not)
    le = toktype('Le') >> const(Le)
    ge = toktype('Ge') >> const(Ge)

    point_op = mul | div
    line_op = add | sub
    comp_op = lt | gt | eq | orop | andop | neq | notop | le | ge

    assign = with_forward_decls(lambda: toktype('Ident') + skip(toktype('Assign')) + exp >> unarg(Assignment))
    ifexp = with_forward_decls(lambda: ident_('if') + cond + cmd + \
                                       maybe(ident_('else') + cmd) >> unarg(IfThenElse))
    whileexp = with_forward_decls(lambda: ident_('while') + cond + cmd >> unarg(While))
    printexp = with_forward_decls(lambda: ident_('print') + exp >> Print)
    vardef = with_forward_decls(lambda: ident_('var') + toktype('Ident') + op_('=') + exp \
                                        >> unarg(Declaration))

    cmd = with_forward_decls(lambda: assign | ifexp | whileexp | printexp | vardef | \
                                        skip(toktype('Lb')) + cmd_list + skip(toktype('Rb')))
    cmd_list = (cmd + many(skip(toktype('Semicolon')) + cmd) >> lst) >> CmdList

    variable = toktype('Ident') >> Variable
    constexp = toktype('Number') >> Const
    factor = with_forward_decls(lambda: variable | constexp | \
                                        skip(toktype('Lp')) + exp + skip(toktype('Rp')))
    summand = factor + many(point_op + factor) >> unarg(eval_expr)
    exp = with_forward_decls(lambda: summand + many(line_op + summand) >> unarg(eval_expr) | \
                                        cond)

    cond = exp + comp_op + exp >> eval_cond

    return cmd.parse(seq)

parsed = parse(tokenize('{ var x = 5; print x }'))
print(str(parsed))
parsed.eval(Env())

