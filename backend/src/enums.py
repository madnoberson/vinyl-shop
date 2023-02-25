from enum import IntEnum


class ScopesIntEnum(IntEnum):
    stats = 2 ** 1
    edit = 2 ** 2
    support = 2 ** 3
    admin = 2 ** 4
