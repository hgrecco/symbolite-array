# symbolite-array: an array extension from symbolite

______________________________________________________________________

[Symbolite](https://github.com/hgrecco/symbolite) allows you to
create symbolic mathematical expressions. Just create a symbol
(or more) and operate with them as you will normally do in Python.

This extension allows you to use arrays

```python
>>> from symbolite.abstract import array
>>> arr = array.Array("arr")
>>> expr1 = arr + 1
>>> print(expr1)
(arr + 1)
```

and you can get one item.

```python
>>> from symbolite.abstract import array
>>> arr = array.Array("arr")
>>> expr2 = arr[1] + 1
>>> print(expr2)
(arr[1] + 1)
```

You can easily replace the symbols by the desired value.

```python
>>> expr3 = expr2.replace_by_name(arr=(1, 2, 3))
>>> print(expr3)
((1, 2, 3)[1] + 1)
```

and evaluate:

```python
>>> print(expr3.eval())
3
```

Included in this library are implementations for `sum` and `prod`,
in the default implementation (based on python's math), NumPy, and
SciPy. In SciPy, `Array` is also mapped to SciPy's `IndexedBase`.

## Vectorizing expresion

If you have an expression with a number of scalars, you can convert it
into an expresion using a vector with scalar symbols occuping specific
places within the array.

```python
>>> from symbolite.abstract import scalar
>>> x = scalar.Scalar("x")
>>> y = scalar.Scalar("y")
>>> print(array.vectorize(x + scalar.cos(y), ("x", "y")))
(arr[0] + libscalar.cos(arr[1]))
```

The first argument is the expression and the second list (in order)
the scalars to be replaced by the array. You can also use a dictionary
mapping scalars names to indices

```python
>>> print(array.vectorize(x + scalar.cos(y), dict(x=3, y=5)))
(arr[3] + libscalar.cos(arr[5]))
```

If you want to replace all scalars automatically, auto

```python
>>> from symbolite.abstract import scalar
>>> x = scalar.Scalar("x")
>>> y = scalar.Scalar("y")
>>> names, vexpr = array.auto_vectorize(x + scalar.cos(y))
>>> print(names) # names are given in the order of the array.
('x', 'y')
>>> print(vexpr)
(arr[0] + libscalar.cos(arr[1]))
```

### Installing:

```bash
pip install -U symbolite-array
```
