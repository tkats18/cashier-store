import random
from typing import Protocol

from shop import IStoreAdministration, IStoreFileSystemAnalyzer
from store_printer import LoggerType, log_store_message


class IReportGenerator(Protocol):
    def generate_report_by_desire(self) -> bool:
        pass


class IShiftEnder(Protocol):
    def end_shift_by_desire(self) -> bool:
        pass


class StoreManager:
    def __init__(
        self,
        file_system_access: IStoreFileSystemAnalyzer,
        shop_administrator: IStoreAdministration,
    ):
        self.file_system_access = file_system_access
        self.shop_administrator = shop_administrator

    def generate_report_by_desire(self) -> bool:
        if random.choice([True, False]):
            data = self.file_system_access.get_data()
            revenue = self.file_system_access.get_total_revenue()
            report = (
                "\n"
                + "{:10s} {:1s} {:5s} {:1s}".format("Name", "|", "Sold", "|")
                + "\n"
            )
            for i in data:
                report += (
                    "{:10s} {:1s} {:5s} {:1s}".format(i, "|", str(data[i]), "|") + "\n"
                )

            report += "\nTotal Revenue: " + str(revenue)
            log_store_message(LoggerType.MANAGER, "Current report:" + report)
            return True
        else:
            log_store_message(LoggerType.MANAGER, "I chose not to generate report")
            return False

    def end_shift_by_desire(self) -> bool:
        if random.choice([True, False]):
            log_store_message(LoggerType.MANAGER, "I chose to end shift")
            self.shop_administrator.close_shift()
            return True
        else:
            log_store_message(LoggerType.MANAGER, "I chose not to end shift")
            return False
