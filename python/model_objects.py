from dataclasses import dataclass
from enum import Enum


class ProductUnit(Enum):
    """
    Enumeration for product units.

    Attributes:
        EACH (int): Product is sold by each unit.
        KILO (int): Product is sold by kilogram.
    """

    EACH = 1  # Product is sold by each unit
    KILO = 2  # Product is sold by kilogram


@dataclass
class Product:
    """
    Represents a product with a name and unit.

    Attributes:
        name (str): The name of the product.
        unit (ProductUnit): The unit in which the product is sold.
    """

    # The name of the product
    name: str
    # The unit in which the product is sold
    unit: ProductUnit

    def __hash__(self):
        return hash((self.name, self.unit))


@dataclass
class ProductQuantity:
    """
    Represents a quantity of a product.

    Attributes:
        product (Product): The product being represented.
        quantity (float): The quantity of the product.
    """

    # The product being represented
    product: Product
    # The quantity of the product
    quantity: float


class OfferType(Enum):
    """
    Enumeration for special offer types.

    Attributes:
        THREE_FOR_TWO (int): Three products for the price of two.
        TEN_PERCENT_DISCOUNT (int): Ten percent discount on the product.
        TWO_FOR_AMOUNT (int): Two products for a specified amount.
        FIVE_FOR_AMOUNT (int): Five products for a specified amount.
    """

    THREE_FOR_TWO = 1  # Three products for the price of two
    TEN_PERCENT_DISCOUNT = 2  # Ten percent discount on the product
    TWO_FOR_AMOUNT = 3  # Two products for a specified amount
    FIVE_FOR_AMOUNT = 4  # Five products for a specified amount


@dataclass
class Offer:
    """
    Represents an offer with a type and argument.

    Attributes:
        offer_type (OfferType): The type of the offer.
        argument (float): The argument for the offer, which depends on the offer type.
    """

    # The type of the offer (e.g. three for two, ten percent discount, etc.)
    offer_type: OfferType
    # The argument for the offer (e.g. the amount for a two for amount offer)
    argument: float


@dataclass
class Discount:
    """
    Represents a discount with a product, description, and amount.

    Attributes:
        product (Product): The product associated with the discount.
        description (str): A brief description of the discount.
        discount_amount (float): The amount of the discount.
    """

    # The product associated with the discount
    product: Product
    # A brief description of the discount (e.g. "three for two")
    description: str
    # The amount of the discount (negative value indicates a discount)
    discount_amount: float
