from __future__ import annotations

import time
from collections.abc import Iterable, Iterator
from itertools import islice
from typing import Callable, TypeVar

T = TypeVar("T")


def batched(iterable: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    """
    Returns a batch of the provided size from the provided iterable.
    """
    iterator = iter(iterable)
    while True:
        batch = tuple(islice(iterator, size))
        if not batch:
            break
        yield batch


def waiter(timeout: float | None = None) -> Callable[[float], bool]:
    """
    Waiter returns a wait function that sleeps the specified amount of seconds, and
    handles timeouts.

    The wait function returns True if the timeout was reached, False otherwise.

    :param timeout: Timeout in seconds, defaults to None.
    :return: Wait function.
    """

    if timeout:
        deadline = time.time() + timeout

        def wait(seconds: float) -> bool:
            now = time.time()

            # Timeout if the deadline exceeded.
            if deadline < now:
                return True

            # The deadline is not exceeded after the sleep time.
            if now + seconds < deadline:
                time.sleep(seconds)
                return False

            # The deadline is exceeded after the sleep time, clamp sleep time to
            # deadline, and allow one last attempt until next wait call.
            time.sleep(deadline - now)
            return False

    else:

        def wait(seconds: float) -> bool:
            time.sleep(seconds)
            return False

    return wait
