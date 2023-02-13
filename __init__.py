import abc
import collections.abc
import functools
import typing

A = typing.TypeVar(name='A')
B = typing.TypeVar(name='B')


class AbstractBijection(collections.abc.MutableMapping[A, B], abc.ABC):

    @property
    @abc.abstractmethod
    def inv(self) -> 'AbstractBijection':
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def _forwards(self) -> dict[A, B]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def _backwards(self) -> dict[B, A]:
        raise NotImplementedError

    def __iter__(self) -> typing.Iterator[A]:
        return iter(self._forwards)

    def __len__(self) -> int:
        return len(self._forwards)

    def __getitem__(self, a: A) -> B:
        return self._forwards[a]

    def __setitem__(self, a: A, b: B):
        self._put(self._forwards, self._backwards, a, b)
        self._put(self._backwards, self._forwards, b, a)

    def __delitem__(self, a: A) -> None:
        b = self._forwards.pop(a)
        assert self._backwards.pop(b) == a

    def _put(self, forwards: dict[A, B], backwards: dict[B, A], a: A, b: B):
        try:
            old_b = forwards[a]
        except KeyError:
            forwards[a] = b
        else:
            if old_b != b:
                assert backwards.pop(old_b) == a
                forwards[a] = b


class Bijection(AbstractBijection[A, B]):
    """
    >>> b = Bijection(); b
    Bijection({})
    >>> b.inv
    BijectionMirror({})

    >>> b = Bijection([(1, 2), (3, 4)]); b
    Bijection({1: 2, 3: 4})
    >>> b.inv
    BijectionMirror({1: 2, 3: 4})

    >>> b = Bijection([(1, 1), (1, 2), (1, 3)]); b
    Bijection({1: 3})
    >>> b.inv
    BijectionMirror({1: 3})


    >>> b = Bijection([(1, 1), (2, 1), (3, 1)]); b
    Bijection({3: 1})
    >>> b.inv
    BijectionMirror({3: 1})

    >>> b[2] = 4; b
    Bijection({3: 1, 2: 4})

    >>> b.inv[2] = 4; b
    Bijection({3: 1, 2: 4, 4: 2})

    >>> del b[4]; b
    Bijection({3: 1, 2: 4})

    >>> del b.inv[4]; b
    Bijection({3: 1})
    """

    def __init__(self, items: typing.Iterable[tuple[A, B]] = ()):
        self._a2b = dict(items)
        self._b2a = {}
        for a, b in list(self.items()):
            self._put(self._backwards, self._forwards, b, a)

    @functools.cached_property
    def inv(self) -> 'BijectionMirror':
        return BijectionMirror(self)

    @property
    def _forwards(self) -> dict[A, B]:
        return self._a2b

    @property
    def _backwards(self) -> dict[B, A]:
        return self._b2a

    def __repr__(self):
        cls = type(self)
        return f'{cls.__name__}({self._forwards})'

    def values(self) -> typing.KeysView[B]:
        return self.inv.keys()


class BijectionMirror(AbstractBijection[B, A]):

    def __init__(self, origin: Bijection):
        self._origin = origin

    @property
    def inv(self) -> Bijection:
        return self._origin

    @property
    def _forwards(self) -> dict[B, A]:
        return self._origin._backwards

    @property
    def _backwards(self) -> dict[A, B]:
        return self._origin._forwards

    def __repr__(self):
        cls = type(self)
        return f'{cls.__name__}({self._backwards})'

