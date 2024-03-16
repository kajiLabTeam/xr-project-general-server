import random

from ulid import ULID


def generate_ulid() -> ULID:
    random.seed()
    return ULID()
