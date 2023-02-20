from enum import IntEnum


class ScopesEnum(IntEnum):
    stats = 2
    edit = 2 ** 2
    support = 2 ** 3
