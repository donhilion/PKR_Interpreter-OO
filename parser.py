from functools import reduce
from re import VERBOSE
from funcparserlib.lexer import make_tokenizer, Token
from funcparserlib.parser import some, a, skip, with_forward_decls, many, maybe
from ast import Add, Sub, Mul, Div, Lt, Gt, Eq, Or, And, Neq, Not, Le, Ge, Assignment, IfThenElse, While, Print, Declaration, CmdList, Variable, Const, Function, Call, Object, Dot, Class, New
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
        ('Dot',         ('\.',)),
        ('Op',          (r'[\-+/*=<>]',)),
        ('Ident', 		(r'[A-Za-z][A-Za-z_0-9]*',)),
        ('Number',      (r'(0|([1-9][0-9]*))', VERBOSE)),
        ('Semicolon',	(';',)),
        ('Comma',	    (',',)),
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
    arglst = with_forward_decls(lambda: exp + many(skip(toktype('Comma')) + exp) >> lst)
    returnexp = with_forward_decls(lambda: ident_('return') + exp)
    call = with_forward_decls(lambda: dot + skip(toktype('Lp') + toktype('Rp')) >> unarg(Call) | \
                                      dot + skip(toktype('Lp')) + arglst + skip(toktype('Rp')) >> unarg(Call))
    args = toktype('Ident') + many(skip(toktype('Comma')) + toktype('Ident')) >> lst
    decl = with_forward_decls(lambda: toktype('Ident') + op_('=') + exp >> unarg(Declaration))
    decls = decl + many(skip(toktype('Semicolon')) + decl) >> lst
    classdecl = ident_('class') + toktype('Ident') + op_('=') + skip(toktype('Lp')) + args + skip(toktype('Rp')) \
                + skip(toktype('Lp')) + maybe(toktype('Ident')) + skip(toktype('Rp') + \
                toktype('Lb')) + decls + skip(toktype('Rb')) >> unarg(Class)
    newexp = ident_('new') + toktype('Ident') + skip(toktype('Lp') + toktype('Rp')) >> New | \
             ident_('new') + toktype('Ident') + skip(toktype('Lp')) + arglst + skip(toktype('Rp')) >> New

    cmd = with_forward_decls(lambda: call | returnexp | assign | ifexp | whileexp | printexp | vardef | classdecl | \
                                        skip(toktype('Lb')) + cmd_list + skip(toktype('Rb')))
    cmd_list = (cmd + many(skip(toktype('Semicolon')) + cmd) >> lst) >> CmdList

    variable = toktype('Ident') >> Variable
    dotop = toktype('Dot') >> const(Dot)
    dot = newexp  + many(dotop + toktype('Ident')) >> unarg(eval_expr) | variable  + many(dotop + toktype('Ident')) >> unarg(eval_expr)
    constexp = toktype('Number') >> Const
    factor = with_forward_decls(lambda: dot | constexp | \
                                        skip(toktype('Lp')) + exp + skip(toktype('Rp')))
    summand = factor + many(point_op + factor) >> unarg(eval_expr)
    function = ident_('function') + skip(toktype('Lp')) + args + skip(toktype('Rp')) + skip(toktype('Lb')) + cmd_list \
               + skip(toktype('Rb')) >> unarg(Function)
    objectexp = ident_('object') + skip(toktype('Lb')) + decls + skip(toktype('Rb')) >> Object

    exp = with_forward_decls(lambda: objectexp | function | call | newexp | \
                                     summand + many(line_op + summand) >> unarg(eval_expr) | cond)

    cond = exp + comp_op + exp >> eval_cond

    return cmd.parse(seq)

parsed = parse(tokenize('''
    {
        var x = 5;
        var f =
            function(a,b) {
                print a;
                print b;
                return 42;
                print 23
            };
        print x;
        var z = f(2,x);
        print z;

        var o = object {
            field1 = 15;
            field2 = 23;
            fun = function(x) {
                return x+this.field1;
            };
            o = object {
                inner = 42;
            };
        };
        print o.field1;
        print o.fun(4);
        print o.o.inner;

        class foo = (a, b)() {
            foo = a;
            bar = b;
        };

        var obj = new foo(1, 2);
    }'''))
print(str(parsed))
parsed.eval(Env())
