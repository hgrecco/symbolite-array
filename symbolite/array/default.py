"""
    symbolite.impl.array.default
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Translate symbolite.abstract.array into values and functions
    defined in Python's math module.

    :copyright: 2023 by Symbolite-array Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import math
import operator

from symbolite.core.translators import Unsupported

op_getitem = operator.getitem

sum = math.fsum
prod = math.prod

Array = Unsupported
