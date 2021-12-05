import json
from abc import abstractmethod
from typing import Dict, List, Protocol

from product import Product


class IProductListReader(Protocol):
    def read_product_source(self) -> List[Product]:
        pass


# როგორც დისქაუნთების ისევე პროდუქტები საიდანღაც ხომ უნდა მივიღოთ
# ამიტომ სტრატეგიაა ესეც და არგუმენტად რახან მეპი გადაეცემა და ვთქვათ
# ბაზიდან ან ფაილიდან ან სერვერიდან გვინდა წამოღება მეპი open-closed
# არ არღვევს კონკრეტულმა იმპლემენტაციამ იცის რასაც ელოდება..


class BaseProductListReader:
    def __init__(self, access_params: Dict[str, str]):
        self.access_params = access_params

    @abstractmethod
    def read_product_source(
        self,
    ) -> List[Product]:
        pass

    def __call__(self) -> List[Product]:
        return self.read_product_source()


class ProductListReaderFromFile(BaseProductListReader):
    def read_product_source(self) -> List[Product]:
        path = self.access_params["path"]
        f = open(path)
        data = json.load(f)

        product_arr = []
        for i in data["products"]:
            # product_map = decoder.decode(i)
            product_arr.append(
                Product(name=i["name"], units=i["units"], price=float(i["price"]))
            )

        return product_arr
