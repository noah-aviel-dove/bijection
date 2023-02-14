import abc
import collections.abc
import functools
import typing


A = typing.TypeVar(name='A')
B = typing.TypeVar(name='B')


class AbstractBijection(collections.abc.MutableMapping[A, B], abc.ABC):

    @property
    @abc.abstractmethod
    def inv(self) -> 'AbstractBijection[B, A]':
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def _mapping(self) -> typing.MutableMapping[A, B]:
        raise NotImplementedError

    def __repr__(self):
        cls = type(self)
        return f'{cls.__name__}({self._mapping})'

    def __iter__(self) -> typing.Iterator[A]:
        return iter(self._mapping)

    def __len__(self) -> int:
        return len(self._mapping)

    def __getitem__(self, a: A) -> B:
        return self._mapping[a]

    def __setitem__(self, a: A, b: B):
        self._put(a, b)
        self.inv._put(b, a)

    def __delitem__(self, a: A) -> None:
        old_b = self._mapping.pop(a)
        self.inv._check_pop(old_b, a)

    def _put(self, a: A, b: B) -> None:
        old_b = self._mapping.setdefault(a, b)
        if old_b != b:
            self._mapping[a] = b
            self.inv._check_pop(old_b, a)

    def _check_pop(self, a: A, expected_b: B) -> None:
        b = self._mapping.pop(a)
        if expected_b != b:
            found, expected = {a: b}, {a: expected_b}
            raise RuntimeError(f'Invalid mapping found in Bijection: {found} should be {expected}')


class Bijection(AbstractBijection[A, B]):
    """
    >>> b = Bijection(); b
    Bijection({})
    >>> b.inv
    BijectionMirror({})
    >>> b.inv.inv is b
    True

    >>> b = Bijection([(1, 2), (3, 4)]); b
    Bijection({1: 2, 3: 4})
    >>> b.inv
    BijectionMirror({2: 1, 4: 3})

    # Like normal dictionaries, later values overwrite earlier ones when there
    # are duplicated keys
    >>> b = Bijection([(1, 1), (1, 2), (1, 3)]); b
    Bijection({1: 3})
    >>> b.inv
    BijectionMirror({3: 1})

    # This also applies to the inverse view: when there are duplicated
    # values, the earlier keys are silently dropped.
    >>> b = Bijection([(1, 1), (2, 1), (3, 1)]); b
    Bijection({3: 1})
    >>> b.inv
    BijectionMirror({1: 3})

    >>> b[2] = 4; b
    Bijection({3: 1, 2: 4})
    >>> b.inv
    BijectionMirror({1: 3, 4: 2})

    >>> b.inv[2] = 4; b
    Bijection({3: 1, 2: 4, 4: 2})
    >>> b.inv
    BijectionMirror({1: 3, 4: 2, 2: 4})


    >>> b.pop(4), b
    (2, Bijection({3: 1, 2: 4}))
    >>> b.inv
    BijectionMirror({1: 3, 4: 2})

    >>> b.inv.pop(4), b
    (2, Bijection({3: 1}))
    >>> b.inv
    BijectionMirror({1: 3})
    """

    def __init__(self, items: typing.Iterable[tuple[A, B]] = ()):
        self._a2b = {}
        self._b2a = {}
        for a, b in items:
            self[a] = b

    @functools.cached_property
    def inv(self) -> 'BijectionMirror[B, A]':
        return BijectionMirror(self)

    @property
    def _mapping(self) -> dict[A, B]:
        return self._a2b


class BijectionMirror(AbstractBijection[B, A]):

    def __init__(self, origin: Bijection[A, B]):
        self._origin = origin

    @property
    def inv(self) -> Bijection[A, B]:
        return self._origin

    @property
    def _mapping(self) -> dict[B, A]:
        # noinspection PyProtectedMember
        return self._origin._b2a
