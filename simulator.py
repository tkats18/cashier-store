from cashier import Cashier
from customer import Customer
from discount_manager import DiscountManager
from discount_strategies import FileIDiscountDataAcquiringStrategy
from paying_strategy import RandomPaymentSelector
from shop import Store, StoreFileSystem
from shop_strategies import ProductListReaderFromFile
from shopping_strategies import RandomShoppingStrategy
from simulator_chain import (CashierReceiptFillHandler,
                             CashierReceiptOpenHandler,
                             CashierReceiptPaymentAcceptHandler,
                             CustomerChooserHandler, CustomerPaymentHandler,
                             ManagerReportGenerateHandler,
                             ManagerShiftEndHandler, Request)
from store_manager import StoreManager


def simulate_single_cashier_single_customer() -> bool:
    args = dict()
    args["path"] = "./data/products.json"

    file_system = StoreFileSystem()
    shop = Store(ProductListReaderFromFile(args), file_system)

    args = dict()
    args["path"] = "./data/discounts.json"
    discount_manager = DiscountManager(FileIDiscountDataAcquiringStrategy(args))

    cashier = Cashier(discount_manager, file_system)
    customer = Customer(shop, RandomShoppingStrategy(), RandomPaymentSelector())
    manager = StoreManager(file_system, shop)
    customer_num = 0

    while shop.shift < 3:
        # ეს ცალცალკე ხაზებზე იმიტოა რო კარგადაა წაკითხვადი ისე chain responsibility არი

        report_generate = ManagerReportGenerateHandler(cur_manager=manager)
        shift_end = ManagerShiftEndHandler(
            cur_manager=manager, next_handler=report_generate
        )
        payment_accept = CashierReceiptPaymentAcceptHandler(
            cashier, next_handler=shift_end
        )
        payment = CustomerPaymentHandler(
            cur_customer=customer, next_handler=payment_accept
        )
        receipt_fill = CashierReceiptFillHandler(cashier, next_handler=payment)
        receipt_open = CashierReceiptOpenHandler(cashier, next_handler=receipt_fill)
        handler = CustomerChooserHandler(
            next_handler=receipt_open, cur_customer=customer
        )

        handler.handle(Request(None, None, None, customer_num))
        customer_num += 1

    return True
