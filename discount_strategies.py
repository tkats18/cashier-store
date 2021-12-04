import json
from abc import abstractmethod
from enum import Enum
from typing import Protocol, Dict

from dicount import IDiscountableProductList, DiscountableProductList, DiscountableProduct, IDiscountData, \
    DiscountDataBuilder


class DiscountType(Enum):
    TOTAL = "TOTAL",
    SINGLE = "SINGLE",
    GROUP = "GROUP"


# დისქაუნთების შესახებ მონახემების სტრატეგიაა ეს. ანუ როგორღაც ხომ უნდა
# იცოდეს მაღაზიამ დისქაუნთების შესახებ სწორი ინფორმაცია საიდან წამოიღოს
# ხოდა როგორც სტატეგია ისე გავიტანე, რეალურ შემთხვევაში შეილაბ ბაზიდან მოდიოდეს,
# ან ფაილიდან, ან სტრიმიდან..

# მეპში ქი იმიტომ არის ლისტი რომ პირობის მიხედვით ყველაზე ზოგადი (რომელიც ყველას
# მოიცავს) შემთხვევა არის როცა ნაყიდი პროდუქტების სია განსაზღვრავს დისქუნთს, ამიტომ
# ეგ ავიღე ქიდ. open-closed არ არღვევს წესით სიის გარდა ვერ წარმომიდგენია უფრო ზოგადი
# რა შეიძლება იყოს საჭირო...

# დაბრუნების ეს ტიპი ნიშნავს რომ დისქუნთების არაი გვაქვს რომელშიც გაწერილია
# კონკრეტული დისქაუნთის კონფიგურაცია. კონკრეტული დისქაუნთის კონფიგურაცია
# მოიაზრებს პროდუქტების(შეკვრაში/არაშეკვრაში) ლისტის არსებობის შემთხვევაში
# მეპს
class IDiscountDataAcquiringStrategy(Protocol):
    def get_discount_data(self) -> Dict[IDiscountableProductList, IDiscountData]:
        pass


class BaseIDiscountDataAcquiringStrategy:

    def __init__(self, access_params: Dict):
        self.access_params = access_params

    @abstractmethod
    def get_discount_data(self) -> Dict[IDiscountableProductList, IDiscountData]:
        pass

    def __call__(self) -> Dict[IDiscountableProductList, IDiscountData]:
        return self.get_discount_data()


class FileIDiscountDataAcquiringStrategy(BaseIDiscountDataAcquiringStrategy):
    def get_discount_data(self) -> Dict[IDiscountableProductList, IDiscountData]:
        path = self.access_params["path"]
        f = open(path)
        data = json.load(f)
        discount_data = dict()

        for i in data['discounts']:

            discount_data_builder = DiscountDataBuilder()
            if i['type'] == DiscountType.TOTAL.name:
                discount_data_builder.with_total_discount(total_amount=i['discount_amount'])

            if i['type'] == DiscountType.SINGLE.name or i['type'] == DiscountType.GROUP.name:
                for cur_prod in i['products']:
                    discount_data_builder.with_discount(DiscountableProduct(cur_prod['name'], cur_prod['units']),
                                                        i['discount_amount'])

            discount_data[DiscountableProductList(list(
                map(lambda x: DiscountableProduct(name=x['name'], units=x['units']),
                    i['products'])))] = discount_data_builder.build()

        return discount_data
