from enum import Enum, IntFlag, IntEnum


class MediaTypes(IntEnum):
    IMAGE = 1
    VIDEO = 2
    AUDIO = 3
    PRESENTATION = 4
    PDF = 5
    TEST = 6
    FILE = 7


class PersonalInformationTypes(str, Enum):
    BOOKMARK = "BOOKMARK"
    NOTE = "NOTE"


class UserPermissions(IntFlag):
    NONE = 0
    ADMINISTRATOR = 1 << 0


class ItemTypes(IntEnum):
    LOST = 1
    FOUND = 2


class ItemStatus(IntEnum):
    ACTIVE = 1
    CLOSED = 2
