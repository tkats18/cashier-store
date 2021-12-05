from enum import Enum

logger = True


class LoggerType(Enum):
    MANAGER = ("MANAGER",)
    CASHIER = ("CASHIER",)
    CUSTOMER = ("CUSTOMER",)
    STORE = ("STORE",)
    FILE_SYSTEM = "FILE_SYSTEM"


def log_store_message(who: LoggerType, message: str) -> None:
    if logger:
        print("{:10s} {:4s}  {:50s}".format(who.name, "-- ", message))
