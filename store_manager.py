import random
from typing import Protocol

from shop import IStoreFileSystemAnalyzer, IStoreAdministration
from store_printer import log_store_message, LoggerType


class IReportGenerator(Protocol):
    def generate_report_by_desire(self):
        pass


class IShiftEnder(Protocol):
    def end_shift_by_desire(self):
        pass


class StoreManager:

    def __init__(self, file_system_access: IStoreFileSystemAnalyzer, shop_administrator: IStoreAdministration):
        self.file_system_access = file_system_access
        self.shop_administrator = shop_administrator

    def generate_report_by_desire(self):
        if random.choice([True, False]):
            data = self.file_system_access.get_data()
            revenue = self.file_system_access.get_total_revenue()
            report = "\n" + '{:10s} {:1s} {:5s} {:1s}'.format("Name", "|", "Sold", "|") + "\n"
            for i in data:
                report += '{:10s} {:1s} {:5d} {:1s}'.format(i, "|", data[i], "|") + "\n"

            report += "\nTotal Revenue: " + str(revenue)
            log_store_message(LoggerType.MANAGER, "Current report:" + report)

        else:
            log_store_message(LoggerType.MANAGER, "I chose not to generate report")

    def end_shift_by_desire(self):
        if random.choice([True, False]):
            log_store_message(LoggerType.MANAGER, "I chose to end shift")
            self.shop_administrator.close_shift()
        else:
            log_store_message(LoggerType.MANAGER, "I chose not to end shift")
