from dataclasses import dataclass
from typing import Optional

from cashier import IReceiptOpener, IReceiptFiller, IPaymentConfirm
from customer import IProductChooser, IPayer
from product import IProducts
from receipt import Receipt
from store_manager import IReportGenerator, IShiftEnder


@dataclass
class Request:
    products: Optional[IProducts]
    receipt: Optional[Receipt]
    paid_amount: Optional[float]
    customer_num: int


class Handler:
    def __init__(self, next_handler: Optional["Handler"] = None):
        self.next_handler = next_handler

    def handle(self, request: Request) -> None:
        if self.next_handler:
            self.next_handler.handle(request)


class CustomerChooserHandler(Handler):
    def __init__(self, cur_customer: IProductChooser, next_handler: Optional["Handler"] = None):
        super().__init__(next_handler)
        self.cur_customer = cur_customer

    def handle(self, req: Request) -> None:
        req.products = self.cur_customer.choose_products()
        super().handle(req)


class CustomerPaymentHandler(Handler):

    def __init__(self, cur_customer: IPayer, next_handler: Optional["Handler"] = None):
        super().__init__(next_handler)
        self.cur_customer = cur_customer

    def handle(self, req: Request) -> None:
        req.paid_amount = self.cur_customer.pay(req.receipt)
        super().handle(req)


class CashierReceiptOpenHandler(Handler):

    def __init__(self, cur_cashier: IReceiptOpener, next_handler: Optional["Handler"] = None):
        super().__init__(next_handler)
        self.cur_cashier = cur_cashier

    def handle(self, req: Request) -> None:
        req.receipt = self.cur_cashier.open_receipt()
        super().handle(req)


class CashierReceiptFillHandler(Handler):

    def __init__(self, cur_cashier: IReceiptFiller, next_handler: Optional["Handler"] = None):
        super().__init__(next_handler)
        self.cur_cashier = cur_cashier

    def handle(self, req: Request) -> None:
        req.receipt = self.cur_cashier.fill_items_to_receipt(req.receipt, req.products)
        super().handle(req)


class CashierReceiptPaymentAcceptHandler(Handler):

    def __init__(self, cur_cashier: IPaymentConfirm, next_handler: Optional["Handler"] = None):
        super().__init__(next_handler)
        self.cur_cashier = cur_cashier

    def handle(self, req: Request) -> None:
        req.receipt = self.cur_cashier.confirm_payment(req.receipt, req.paid_amount)
        super().handle(req)


class ManagerReportGenerateHandler(Handler):

    def __init__(self, cur_manager: IReportGenerator, next_handler: Optional["Handler"] = None):
        super().__init__(next_handler)
        self.cur_cashier = cur_manager

    def handle(self, req: Request) -> None:
        if req.customer_num % 20 == 0:
            req.receipt = self.cur_cashier.generate_report_by_desire()
            super().handle(req)


class ManagerShiftEndHandler(Handler):

    def __init__(self, cur_manager: IShiftEnder, next_handler: Optional["Handler"] = None):
        super().__init__(next_handler)
        self.cur_cashier = cur_manager

    def handle(self, req: Request) -> None:
        if req.customer_num % 100 == 0:
            req.receipt = self.cur_cashier.end_shift_by_desire()
            super().handle(req)
