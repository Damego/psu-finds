from enum import IntEnum


class ItemTypes(IntEnum):
    LOST = 1
    FOUND = 2


class ItemStatus(IntEnum):
    ACTIVE = 1
    CLOSED = 2
