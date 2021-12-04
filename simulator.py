from cashier import Cashier
from customer import Customer
from customer_strategies import RandomShoppingStrategy
from discount_manager import DiscountManager
from discount_strategies import FileIDiscountDataAcquiringStrategy
from shop import Store, StoreFileSystem
from shop_strategies import ProductListReaderFromFile
from simulator_chain import CustomerChooserHandler, CashierReceiptOpenHandler, CustomerPaymentHandler, \
    CashierReceiptFillHandler, CashierReceiptPaymentAcceptHandler, Request


def simulate_single_cashier_single_customer():
    args = dict()
    args["path"] = "./data/products.json"

    shop = Store(ProductListReaderFromFile(args))

    args = dict()
    args["path"] = "./data/discounts.json"
    discount_manager = DiscountManager(FileIDiscountDataAcquiringStrategy(args))
    storage = StoreFileSystem()

    cashier = Cashier(discount_manager, storage)
    customer = Customer(shop, RandomShoppingStrategy())
    # ეს ცალცალკე ხაზებზე იმიტოა რო კარგადაა წაკითხვადი ისე chain responsibility არი
    payment_accept = CashierReceiptPaymentAcceptHandler(cashier)
    payment = CustomerPaymentHandler(cur_customer=customer, next_handler=payment_accept)
    receipt_fill = CashierReceiptFillHandler(cashier, next_handler=payment)
    receipt_open = CashierReceiptOpenHandler(cashier, next_handler=receipt_fill)
    handler = CustomerChooserHandler(next_handler=receipt_open, cur_customer=customer)

    handler.handle(Request(None, None, None))
