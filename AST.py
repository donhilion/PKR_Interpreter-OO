__author__ = 'Donhilion'

UNDEFINED = None

# leaves of the AST
class Exp(object):

    def eval(self, env):
        return UNDEFINED

class Const(Exp):

    def __init__(self, value):
        self.value = value

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
        if self.variable in env:
            env[self.variable] = self.exp.eval(env)
        else:
            raise Exception('Variable %s not defined.' % self.variable.get_name())

    def __str__(self):
        return "Assignment(%s, %s)" % (self.variable, self.exp)

class Declaration(Exp):

    def __init__(self, variable, exp):
        self.variable = variable
        self.exp = exp

    def eval(self, env):
        if self.variable in env:
            raise Exception('Variable %s already defined.' % self.variable.get_name())
        env[self.variable] = self.exp.eval(env)

    def __str__(self):
        return "Declaration(%s, %s)" % (self.variable, self.exp)

class IfThenElse(Exp):

    def __init__(self, cond, then, els=None):
        self.cond = cond
        self.then = then
        self.els = els

    def eval(self, env):
        if self.cond.eval(env):
            self.then.eval(env)
        elif self.els is not None:
            self.els.eval(env)

    def __str__(self):
        return "If(%s, %s, %s)" % (self.cond, self.then, self.els)

class While(Exp):

    def __init__(self, cond, do):
        self.cond = cond
        self.do = do

    def eval(self, env):
        while self.cond.eval(env):
            self.do.eval(env)

    def __str__(self):
        return "While(%s, %s)" % (self.cond, self.do)

class CmdList(Exp):

    def __init__(self, lst):
        self.lst = lst

    def eval(self, env):
        for cmd in self.lst:
            cmd.eval(env)

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