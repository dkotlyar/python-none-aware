import json

import pytest

from none_aware import Maybe


@pytest.fixture()
def obj():
    class A:
        def __init__(self):
            self.hello = 'world'

        def __json__(self):
            return dict(hello=self.hello)

    return dict(
        foo='bar',
        baz=dict(
            foo='foo',
            bar='bar',
        ),
        arr=[10, 20, 30],
        obj=A(),
    )


@pytest.fixture()
def maybe_obj(obj):
    return Maybe(obj)


@pytest.fixture()
def maybe_strict(obj):
    return Maybe(obj, strict=True)


@pytest.fixture()
def maybe_none():
    return Maybe(None)


def test_value(maybe_obj):
    assert maybe_obj['foo']() == 'bar'
    assert maybe_obj['foo'] == 'bar'
    assert maybe_obj['baz']['foo']() == 'foo'
    assert maybe_obj.foo() == 'bar'
    assert maybe_obj.baz.foo() == 'foo'
    assert maybe_obj.foo.upper() == 'BAR'
    assert maybe_obj.foo.upper.lower() == 'bar'
    assert maybe_obj.bar.foo.other.upper.lower.else_('Nothing') == 'Nothing'
    assert maybe_obj.arr[0]() == 10
    assert maybe_obj.obj.hello() == 'world'


def test_none(maybe_obj):
    assert maybe_obj['bar']() is None
    assert maybe_obj['bar']['foo']() is None
    assert maybe_obj['foo']['bar']() is None
    assert maybe_obj.bar() is None
    assert maybe_obj.bar.foo() is None
    assert maybe_obj.foo.bar() is None
    assert maybe_obj.bar.foo.other.upper.lower() is None
    assert maybe_obj.baz.baz() is None
    assert maybe_obj['baz']['baz']() is None
    assert maybe_obj['baz']['baz']() is None
    assert maybe_obj.arr[10]() is None
    assert maybe_obj.arr['bar']() is None
    assert maybe_obj.obj[10]() is None
    assert maybe_obj.obj.world() is None


def test_is_none(maybe_obj):
    assert maybe_obj['bar'].is_none()
    assert maybe_obj['bar']['foo'].is_none()
    assert maybe_obj['foo']['bar'].is_none()
    assert maybe_obj.bar.is_none()
    assert maybe_obj.bar.foo.is_none()
    assert maybe_obj.foo.bar.is_none()
    assert maybe_obj.bar.foo.other.upper.lower.is_none()
    assert not maybe_obj.foo.is_none()


def test_strict_value(maybe_strict):
    assert maybe_strict['foo'].else_('Other') == 'bar'
    assert maybe_strict.foo.else_('Other') == 'Other'


def test_maybe_none(maybe_none):
    assert maybe_none.is_none()
    assert maybe_none.foo.bar() is None
    assert maybe_none.bar.baz.is_none()


def test_json(maybe_obj):
    from json import JSONEncoder

    def wrapped_default(self, obj):
        return getattr(obj.__class__, "__json__", wrapped_default.default)(obj)

    wrapped_default.default = JSONEncoder().default
    # apply the patch
    JSONEncoder.original_default = JSONEncoder.default
    JSONEncoder.default = wrapped_default

    assert json.dumps(maybe_obj)
