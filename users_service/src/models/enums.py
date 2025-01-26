from enum import IntFlag


class UserPermissions(IntFlag):
    NONE = 0
    ADMINISTRATOR = 1 << 0
