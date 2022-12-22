"""
    symbolite.abstract.array
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Function and values for array operations.

    :copyright: 2022 by Symbolite-array Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import annotations

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


def vectorize(
    expr: SymbolicExpression,
    symbol_names: tuple[str, ...] | dict[str, int],
    varname="arr",
) -> SymbolicExpression:
    """Vectorize expression by replacing scalar symbols
    by an array at a given indices.

    Parameters
    ----------
    expr
    symbol_names
        if a tuple, provides the names of the symbols
        which will be mapped to the indices given by their position.
        if a dict, maps symbol names to indices.
    varname
        name of the array variable
    """
    if isinstance(symbol_names, dict):
        it = zip(symbol_names.values(), symbol_names.keys())
    else:
        it = enumerate(symbol_names)

    arr = Array(varname)

    reps = {scalar.Scalar(name): arr[ndx] for ndx, name in it}
    return expr.replace(reps)


def auto_vectorize(expr, varname="arr") -> tuple[tuple[str, ...], SymbolicExpression]:
    """Vectorize expression by replacing all scalar symbols
    by an array at a given indices. Symbols are ordered into
    the array alphabetically.

    Parameters
    ----------
    expr
    varname
        name of the array variable

    Returns
    -------
    tuple[str, ...]
        symbol names as ordered in the array.
    SymbolicExpression
        vectorized expression.
    """
    symbol_names = tuple(sorted(expr.symbol_names("")))
    return symbol_names, vectorize(expr, symbol_names, varname)
