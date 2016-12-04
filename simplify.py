from differentiate import Div, Mul, Add, Variable


class Graph:

    def __init__(self, node):
        self.node = node

    def simplify(self):
        names = {Mul: '*', Add: '+', Div: '/'}
        n = self.node

        if hasattr(n, 'a'):
            n.a = Graph(n.a).simplify()
            n.b = Graph(n.b).simplify()
            n.name = '({} {} {})'.format(n.a.name, names[type(n)], n.b.name)

        while hasattr(n, 'a'):
            if isinstance(n, Mul):
                if n.a.fixed and n.b.fixed:
                    val = n.a.val*n.b.val
                    n = Variable(name=str(val), val=val, fixed=True)
                elif n.a.fixed:
                    if n.a.val == 0:
                        n = Variable(name='0', val=0, fixed=True)
                    elif n.a.val == 1:
                        n = n.b
                elif n.b.fixed:
                    if n.b.val == 0:
                        n = Variable(name='0', val=0, fixed=True)
                    elif n.b.val == 1:
                        n = n.a
            elif isinstance(n, Add):
                if n.a.fixed and n.b.fixed:
                    val = n.a.val + n.b.val
                    n = Variable(name=str(val), val=val, fixed=True)
                elif n.a.fixed and n.a.val == 0:
                    n = n.b
                elif n.b.fixed and n.b.val == 0:
                    n = n.a
            elif isinstance(n, Div):
                if n.a.fixed and n.a.val == 0:
                    n = Variable(name='0', val=0, fixed=True)
                elif n.b.fixed and n.b.val == 1:
                    n = n.a
                elif n.a is n.b:
                    n = Variable(name='1', val=1, fixed=True)
            break
        return n
