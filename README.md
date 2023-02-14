# Bijection

A single-file package implementing a mutable, bidirectional, 1-to-1 mapping with
O(1) item access.

Since every key in the bijection is also a value and vice-versa, the generic
type parameters `A` and `B` are used in place of the traditional `K` and `V`.
An instance of `AbstractBijection[A, B]` implements
`typing.MutableMapping[A, B]`, and exposes an attribute called `inv` which is an
instance of `AbstractBijection[B, A]` and provides an inverted view of its
parent object. Both the bijection and its inverse support O(1) lookup and
deletion.

Usually, `Bijection` is the only class that you will need to explicitly
instantiate. `AbstractBijection` is usually a more correct choice for use in
type annotations.

See the doctests for examples.
