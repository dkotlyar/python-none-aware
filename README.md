# Python none-aware

## Install

```commandline
pip install none-aware
```

## Usage

```python
from none_aware import Maybe
obj = dict(foo='bar', baz=dict(foo='foo', bar='bar'))

maybe_obj = Maybe(obj)

assert maybe_obj['foo']() == 'bar'
assert maybe_obj['bar']() is None
assert maybe_obj['baz']['foo']() == 'foo'
assert maybe_obj['bar']['foo']() is None
assert maybe_obj['foo']['bar']() is None
assert maybe_obj.foo() == 'bar'
assert maybe_obj.bar() is None
assert maybe_obj.baz.foo() == 'foo'
assert maybe_obj.bar.foo() is None
assert maybe_obj.foo.bar() is None
assert maybe_obj.foo.upper() == 'BAR'
assert maybe_obj.foo.upper.lower() == 'bar'
assert maybe_obj.bar.foo.other.upper.lower() is None
assert maybe_obj.bar.foo.other.upper.lower.else_('Nothing') == 'Nothing'

maybe_strict = Maybe(obj, strict=True)
assert maybe_strict['foo'].else_('Other') == 'bar'
assert maybe_strict.foo.else_('Other') == 'Other'

maybe_none = Maybe(None)
print(maybe_none.foo.bar)  # None
print(maybe_none.is_none())  # True
print(maybe_none.bar.baz.is_none())  # True
print(maybe_obj.foo.is_none())  # False
print(maybe_obj.foo.bar.is_none())  # True
```
