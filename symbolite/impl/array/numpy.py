"""
    symbolite.impl.array.numpy
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Translate symbolite.abstract.array into values and functions
    defined in NumPy.

    :copyright: 2022 by Symbolite-array Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import operator

import numpy as np
from symbolite.translators import Unsupported

op_getitem = operator.getitem

sum = np.sum
prod = np.prod

Array = Unsupported
