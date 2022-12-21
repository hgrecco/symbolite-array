import pytest
from symbolite.mappers import Unsupported

from symbolite.abstract import array, scalar
from symbolite.impl.array import default

all_impl = {"default": default}

try:
    from symbolite.impl.array import numpy as npm

    all_impl["numpy"] = npm
except ImportError:
    pass

try:
    from symbolite.impl.array import sympy as spm

    all_impl["sympy"] = spm
except ImportError:
    pass


def test_array():
    arr = array.Array("arr")
    assert str(arr) == "arr"
    assert str(arr[1]) == "arr[1]"


def test_methods():
    arr = array.Array("arr")
    assert arr.replace_by_name(arr=(1, 2, 3)) == (1, 2, 3)
    assert arr[1].replace_by_name(arr=(1, 2, 3)).eval() == 2
    assert arr.symbol_names() == {
        "arr",
    }
    assert arr[1].symbol_names() == {
        "arr",
    }
    assert (arr[1] + arr[0]).symbol_names() == {
        "arr",
    }


@pytest.mark.parametrize("libarray", all_impl.values(), ids=all_impl.keys())
def test_impl(libarray):
    v = (1, 2, 3, 4)

    try:
        expr = array.sum(v)
        assert expr.eval(libarray=libarray) == 10
    except Unsupported:
        pass

    expr = array.prod(v)
    assert expr.eval(libarray=libarray) == 24


def test_impl_numpy():
    try:
        import numpy as np
        from symbolite.impl.scalar import numpy as libscalar
    except ImportError:
        return

    v = np.asarray((1, 2, 3))

    expr = array.Array("arr") + 1
    assert np.allclose(expr.replace_by_name(arr=v).eval(), v + 1)

    expr = scalar.cos(array.Array("arr"))

    assert np.allclose(expr.replace_by_name(arr=v).eval(libscalar=libscalar), np.cos(v))


def test_impl_scioy():
    try:
        import sympy as sy

        from symbolite.impl.array import sympy as libarray
    except ImportError:
        return

    arr = array.Array("arr")
    syarr = sy.IndexedBase("arr")
    assert arr.eval(libarray=libarray) == syarr
    assert arr[1].eval(libarray=libarray) == syarr[1]
