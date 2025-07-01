from enum import Enum

class AccountStates(int, Enum):
    ACTIVE = 0
    INACTIVE = 1
    BANNED = 2