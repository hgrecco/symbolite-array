import operator

from symbolite.operands import Function, Named, Operator, SymbolicExpression

from symbolite.abstract import scalar

NAMESPACE = "libarray"

op_getitem = Operator.from_operator(operator.getitem, "{}[{}]", NAMESPACE)

sum = Function("sum", namespace=NAMESPACE, arity=1)
prod = Function("prod", namespace=NAMESPACE, arity=1)


class Array(Named, SymbolicExpression):
    def __getitem__(self, item):
        return op_getitem(self, item)


def vectorize(expr, symbol_names, varname="arr"):
    if isinstance(symbol_names, dict):
        it = zip(symbol_names.values(), symbol_names.keys())
    else:
        it = enumerate(symbol_names)

    arr = Array(varname)

    reps = {scalar.Scalar(name): arr[ndx] for ndx, name in it}
    return expr.replace(reps)


def auto_vectorize(expr, varname="arr"):
    symbol_names = sorted(expr.symbol_names(""))
    return symbol_names, vectorize(expr, symbol_names, varname)
