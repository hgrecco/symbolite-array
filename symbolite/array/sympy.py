"""
    symbolite.array.sympy
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Translate symbolite.array.abstract into values and functions
    defined in SymPy.

    :copyright: 2023 by Symbolite-array Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import operator

import sympy as sy

arr = sy.IndexedBase("arr")

op_getitem = operator.getitem

sum = sum
prod = sy.prod

Array = sy.IndexedBase
