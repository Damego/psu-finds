from enum import Enum, IntFlag, IntEnum


class UserPermissions(IntFlag):
    NONE = 0
    ADMINISTRATOR = 1 << 0


class ItemTypes(IntEnum):
    LOST = 1
    FOUND = 2


class ItemStatus(IntEnum):
    ACTIVE = 1
    CLOSED = 2
