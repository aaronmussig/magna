from typing import Sized, Iterator


def get_batches(iterable: Sized, n: int = 1) -> Iterator[Sized]:
    """Generate batches of size n from the iterable.

    Args:
        The iterable to split into batches.
        The size of each batch.

    Returns:
        An iterator with each batch.
    """
    n_iterable = len(iterable)
    for ndx in range(0, n_iterable, n):
        yield iterable[ndx:min(ndx + n, n_iterable)]
