"""
    symbolite.abstract.array
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Function and values for array operations.

    :copyright: 2023 by Symbolite-array Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import annotations

from symbolite.core.operands import Function, OperandMixin
from symbolite.scalar import abstract as scalar
from symbolite.symbol import abstract as symbol

NAMESPACE = "libarray"

sum = Function("sum", namespace=NAMESPACE, arity=1)
prod = Function("prod", namespace=NAMESPACE, arity=1)


class Array(symbol.Symbol):
    pass


def vectorize(
    expr: OperandMixin,
    symbol_names: tuple[str, ...] | dict[str, int],
    varname="arr",
) -> OperandMixin:
    """Vectorize expression by replacing test_scalar symbols
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
    return expr.subs(reps)


def auto_vectorize(expr, varname="arr") -> tuple[tuple[str, ...], OperandMixin]:
    """Vectorize expression by replacing all test_scalar symbols
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
