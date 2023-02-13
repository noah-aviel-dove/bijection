# Bijection

A single-file package implementing a bidirectional 1-to-1 mapping.
This data structure like a dictionary, except that the values also act like keys.
See the doctests for examples of this behavior.
Under the hood it's just two dictionaries.

Conceptually equivalent to a set of ordered pairs, but with O(1) lookup
for pairs based on either the first or second element.
