import pytest
from symbolite.mappers import Unsupported

from symbolite.abstract import array, scalar
from symbolite.impl.array import default

all_impl = {"default": default}

x, y = map(scalar.Scalar, ("x", "y"))
arr = array.Array("arr")
v = array.Array("v")

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


@pytest.mark.parametrize(
    "expr,params,result",
    [
        (x + 2 * y, ("x", "y"), arr[0] + 2 * arr[1]),
        (x + 2 * y, ("y", "x"), arr[1] + 2 * arr[0]),
        (x + 2 * scalar.cos(y), ("y", "x"), arr[1] + 2 * scalar.cos(arr[0])),
        (x + 2 * y, dict(x=3, y=5), arr[3] + 2 * arr[5]),
        (x + 2 * y, dict(x=5, y=3), arr[5] + 2 * arr[3]),
    ],
)
def test_vectorize(expr, params, result):
    assert array.vectorize(expr, params, result)


def test_vectorize_non_default_varname():
    assert array.vectorize(x + 2 * y, ("x", "y"), v[0] + 2 * v[1])


@pytest.mark.parametrize(
    "expr,result",
    [
        (x + 2 * y, (("x", "y"), arr[0] + 2 * arr[1])),
        (y + 2 * x, (("x", "y"), arr[1] + 2 * arr[0])),
        (x + 2 * scalar.cos(y), (("x", "y"), arr[0] + 2 * scalar.cos(arr[1]))),
    ],
)
def test_autovectorize(expr, result):
    assert array.auto_vectorize(expr) == result


def test_autovectorize_non_default_varname():
    assert array.auto_vectorize(x + 2 * y, "v") == (("x", "y"), v[0] + 2 * v[1])
