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

Included in this library are implementations for `sum` and `prod`,
in the default implementation (based on python's math), NumPy, and 
SciPy. In SciPy, `Array` is also mapped to SciPy's `IndexedBase`.


### Installing:

```bash
pip install -U symbolite-array
```