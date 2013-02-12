from env import Env
from heap import heap

__author__ = 'Donhilion'

UNDEFINED = None
NO_RETURN = object()

# leaves of the AST
class Exp(object):

    def eval(self, env):
        return UNDEFINED

    def set_this(self, this):
        pass

class Const(Exp):

    def __init__(self, value):
        self.value = int(value)

    def eval(self, env):
        return self.value

    def __str__(self):
        return "Constant(%s)" % self.value

class Variable(Exp):

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def eval(self, env):
        if self.name not in env:
            return UNDEFINED
        return env[self.name]

    def __str__(self):
        return "Variable(%s)" % self.name

class Assignment(Exp):

    def __init__(self, variable, exp):
        self.variable = variable
        self.exp = exp

    def eval(self, env):
        if self.variable == 'this':
            raise Exception('It is not allowed to declare this.')
        if self.variable == 'true':
            raise Exception('It is not allowed to declare this.')
        if self.variable == 'false':
            raise Exception('It is not allowed to declare this.')
        if self.variable in env:
            env[self.variable] = self.exp.eval(env)
            return NO_RETURN
        else:
            raise Exception('Variable %s not defined.' % self.variable)

    def __str__(self):
        return "Assignment(%s, %s)" % (self.variable, self.exp)

class Declaration(Exp):

    def __init__(self, variable, exp):
        self.variable = variable
        self.exp = exp

    def eval(self, env):
        if self.variable == 'this':
            raise Exception('It is not allowed to declare this.')
        if env.directly_defined(self.variable):
            raise Exception('Variable %s already defined.' % self.variable.get_name())
        env.declare(self.variable, self.exp.eval(env))
        return NO_RETURN

    def __str__(self):
        return "Declaration(%s, %s)" % (self.variable, self.exp)

class IfThenElse(Exp):

    def __init__(self, cond, then, els=None):
        self.cond = cond
        self.then = then
        self.els = els

    def eval(self, env):
        if self.cond.eval(env):
            return self.then.eval(env)
        elif self.els is not None:
            return self.els.eval(env)
        return NO_RETURN

    def __str__(self):
        return "If(%s, %s, %s)" % (self.cond, self.then, self.els)

class While(Exp):

    def __init__(self, cond, do):
        self.cond = cond
        self.do = do

    def eval(self, env):
        while self.cond.eval(env):
            val = self.do.eval(env)
            if val is not NO_RETURN:
                return val
        return NO_RETURN

    def __str__(self):
        return "While(%s, %s)" % (self.cond, self.do)

class CmdList(Exp):

    def __init__(self, lst):
        self.lst = lst

    def eval(self, env):
        new_env = Env(env)
        for cmd in self.lst:
            val = cmd.eval(new_env)
            if val is not NO_RETURN:
                return val
        return NO_RETURN

    def __str__(self):
        string = ""
        for cmd in self.lst:
            string += "%s, " % cmd
        return "CmdList(%s)" % string[:-2]

class Print(Exp):

    def __init__(self, exp):
        self.exp = exp

    def eval(self, env):
        print(self.exp.eval(env))
        return NO_RETURN

    def __str__(self):
        return "Print(%s)" % self.exp

class Add(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) + self.right.eval(env)

    def __str__(self):
        return "Add(%s, %s)" % (self.left, self.right)

class Sub(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) - self.right.eval(env)

    def __str__(self):
        return "Sub(%s, %s)" % (self.left, self.right)

class Mul(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) * self.right.eval(env)

    def __str__(self):
        return "Mul(%s, %s)" % (self.left, self.right)

class Mod(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) % self.right.eval(env)

    def __str__(self):
        return "Mod(%s, %s)" % (self.left, self.right)

class Div(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) / self.right.eval(env)

    def __str__(self):
        return "Div(%s, %s)" % (self.left, self.right)

class Eq(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) == self.right.eval(env)

    def __str__(self):
        return "Eq(%s, %s)" % (self.left, self.right)

class Lt(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) < self.right.eval(env)

    def __str__(self):
        return "Lt(%s, %s)" % (self.left, self.right)

class Gt(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) > self.right.eval(env)

    def __str__(self):
        return "Gt(%s, %s)" % (self.left, self.right)

class Or(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) or self.right.eval(env)

    def __str__(self):
        return "Or(%s, %s)" % (self.left, self.right)

class And(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) and self.right.eval(env)

    def __str__(self):
        return "And(%s, %s)" % (self.left, self.right)

class Neq(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) != self.right.eval(env)

    def __str__(self):
        return "Neq(%s, %s)" % (self.left, self.right)

class Not(Exp):

    def __init__(self, exp):
        self.exp = exp

    def eval(self, env):
        return not self.exp.eval(env)

    def __str__(self):
        return "Not(%s)" % self.exp

class Le(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) <= self.right.eval(env)

    def __str__(self):
        return "Le(%s, %s)" % (self.left, self.right)

class Ge(Exp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) >= self.right.eval(env)

    def __str__(self):
        return "Ge(%s, %s)" % (self.left, self.right)

class Function(Exp):

    def __init__(self, params, cmd):
        self.params = params
        self.cmd = cmd
        self.this = None
        self.env = None

    def eval(self, env):
        if self.env is None:
            self.env = Env(env)
            self.env.declare('this', self.this)
        return self

    def set_this(self, this):
        self.this = this

    def call(self, args, env):
        if len(args) != len(self.params):
            raise Exception("Invalid count of parameters. Should be %s, is %s."  % (len(self.params), len(args)))
        new_env = Env(self.env)
        values = zip(self.params, args)
        for val in values:
            new_env.declare(val[0], val[1])
        return self.cmd.eval(new_env)

    def __str__(self):
        return "Function(%s, %s)" % (self.params, self.cmd)

class Call(Exp):

    def __init__(self, function, exp=None):
        if exp is None:
            exp = []

        self.function = function
        self.exp = exp

    def eval(self, env):
        arglst = []
        for exp in self.exp:
            arglst += [exp.eval(env),]
        return self.function.eval(env).call(arglst, env)

    def __str__(self):
        return "Call(%s, %s)" % (self.function, self.exp)

class Object(Exp):

    def __init__(self, decls):
        self.decls = decls
        self.env = {}

    def eval(self, env):
        new_env = Env(env)
        # put object in heap
        addr = heap.alloc()
        heap[addr] = self

        for decl in self.decls:
            decl.exp.set_this(addr)
            decl.eval(new_env)
        for key in new_env:
            if new_env.directly_defined(key):
                self.env[key] = new_env[key]
        return addr

    def __contains__(self, item):
        return item in self.env

    def __getitem__(self, item):
        return self.env[item]

    def __str__(self):
        return "Object(%s)" % (self.decls)

class Dot(Exp):

    def __init__(self, obj, field):
        self.obj = obj
        self.field = field

    def eval(self, env):
        addr = self.obj.eval(env)
        obj = heap[addr]
        return obj[self.field]

    def __str__(self):
        return "Dot(%s, %s)" % (self.obj, self.field)

class Pointer(Exp):

    def __init__(self, var):
        self.var = var

    def eval(self, env):
        return heap[self.var.eval(env)]

    def get_addr(self, env):
        return self.var.eval(env)

    def __str__(self):
        return "Pointer(%s)" % self.var

class HeapAssign(Exp):

    def __init__(self, variable, exp):
        self.variable = variable
        self.exp = exp

    def eval(self, env):
        addr = self.variable.get_addr(env)
        heap[addr] = self.exp.eval(env)
        return NO_RETURN

    def __str__(self):
        return "HeapAssign(%s, %s)" % (self.variable, self.exp)

class String(Exp):

    def __init__(self, str):
        self.str = str[1:-1]

    def eval(self, env):
        return self.str

    def __str__(self):
        return "String(%s)" % self.str
