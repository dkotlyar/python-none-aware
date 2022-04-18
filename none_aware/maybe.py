class Maybe:
    def __init__(self, value=None, strict=False):
        if isinstance(value, Maybe):
            value = value.else_(None)
        self.__dict__['_value_'] = value
        self.__dict__['_strict_'] = strict

    def else_(self, other):
        return self._value_ if self._value_ is not None else other

    def else_raise(self, error):
        if self._value_ is None:
            raise error
        return self._value_

    def is_none(self):
        return self._value_ is None

    def __json__(self):
        return self._value_

    def __getattr__(self, name):
        if self._value_ is None:
            return Maybe(None)
        if hasattr(self._value_, name):
            attr = getattr(self._value_, name)
            if hasattr(attr, '__call__'):
                attr = attr.__call__()
            return Maybe(attr, strict=self._strict_)
        if not self._strict_:
            return self.__getitem__(name)
        return Maybe(None)

    def __setattr__(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            assert self._value_ is not None
            self._value_.__setattr__(key, value)

    def __getitem__(self, item):
        if self._value_ is None:
            return Maybe(None)
        if hasattr(self._value_, '__getitem__'):
            try:
                return Maybe(self._value_[item], strict=self._strict_)
            except (IndexError, KeyError):
                return Maybe(None)
        if not self._strict_:
            return self.__getattr__(item)
        return Maybe(None)

    def __setitem__(self, key, value):
        assert self._value_ is not None
        self._value_.__setitem__(key, value)

    def __contains__(self, item):
        if hasattr(self._value_, '__getitem__') and item in self._value_:
            return True
        if not self._strict_ and hasattr(self._value_, item):
            return True
        return False

    def __iter__(self):
        if hasattr(self._value_, '__iter__'):
            for item in self._value_:
                yield Maybe(item, strict=self._strict_)

    def __eq__(self, other):
        return self._value_.__eq__(other)

    def __add__(self, other):
        return self._value_.__add__(other)

    def __radd__(self, other):
        return self._value_.__radd__(other)

    def __sub__(self, other):
        return self._value_.__sub__(other)

    def __rsub__(self, other):
        return self._value_.__rsub__(other)

    def __mul__(self, other):
        return self._value_.__mul__(other)

    def __rmul__(self, other):
        return self._value_.__rmul__(other)

    def __matmul__(self, other):
        return self._value_.__matmul__(other)

    def __rmatmul__(self, other):
        return self._value_.__rmatmul__(other)

    def __truediv__(self, other):
        return self._value_.__truediv__(other)

    def __rtruediv__(self, other):
        return self._value_.__rtruediv__(other)

    def __floordiv__(self, other):
        return self._value_.__floordiv__(other)

    def __rfloordiv__(self, other):
        return self._value_.__rfloordiv__(other)

    def __mod__(self, other):
        return self._value_.__mod__(other)

    def __rmod__(self, other):
        return self._value_.__rmod__(other)

    def __divmod__(self, other):
        return self._value_.__divmod__(other)

    def __rdivmod__(self, other):
        return self._value_.__rdivmod__(other)

    def __pow__(self, other, modulo=None):
        return self._value_.__pow__(other, modulo)

    def __rpow__(self, other, modulo=None):
        return self._value_.__rpow__(other, modulo)

    def __lshift__(self, other):
        return self._value_.__lshift__(other)

    def __rlshift__(self, other):
        return self._value_.__rlshift__(other)

    def __rshift__(self, other):
        return self._value_.__rshift__(other)

    def __rrshift__(self, other):
        return self._value_.__rrshift__(other)

    def __and__(self, other):
        return self._value_.__and__(other)

    def __rand__(self, other):
        return self._value_.__rand__(other)

    def __xor__(self, other):
        return self._value_.__xor__(other)

    def __rxor__(self, other):
        return self._value_.__rxor__(other)

    def __or__(self, other):
        if self._value_ is None:
            return Maybe(other)
        if isinstance(other, Maybe):
            return other.__or__(self._value_)
        return self._value_.__or__(other)

    def __ror__(self, other):
        if self._value_ is None:
            return Maybe(other)
        if isinstance(other, Maybe):
            return other.__ror__(self._value_)
        return self._value_.__ror__(other)

    def __repr__(self):
        return self._value_.__repr__()

    def __str__(self):
        return self._value_.__str__()

    def __call__(self, *args, **kwargs):
        return self._value_