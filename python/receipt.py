from model_objects import Product, Discount


class ReceiptItem:
    """
    Represents an item on a receipt.

    Attributes:
        product: The product being purchased.
        quantity: The quantity of the product being purchased.
        price: The price of a single unit of the product.
        total_price: The total price of the product (quantity * price).
    """

    def __init__(
        self, product: Product, quantity: float, price: float, total_price: float
    ):
        """
        Initializes a new ReceiptItem.

        Args:
            product: The product being purchased.
            quantity: The quantity of the product being purchased.
            price: The price of a single unit of the product.
            total_price: The total price of the product (quantity * price).
        """
        self._product: Product = product
        self._quantity: float = quantity
        self._price: float = price
        self._total_price: float = total_price

    @property
    def product(self):
        """
        Returns the product being purchased.

        Returns:
            Product: The product.
        """
        return self._product

    @property
    def quantity(self):
        """
        Returns the quantity of the product being purchased.

        Returns:
            float: The quantity.
        """
        return self._quantity

    @property
    def price(self):
        """
        Returns the price of a single unit of the product.

        Returns:
            float: The price.
        """
        return self._price

    @property
    def total_price(self):
        """
        Returns the total price of the product.

        Returns:
            float: The total price.
        """
        return self._total_price


class Receipt:

    def __init__(self):
        self._items: list[ReceiptItem] = []
        self._discounts: list[Discount] = []

    @property
    def items(self) -> list[ReceiptItem]:
        return self._items[:]

    @property
    def discounts(self) -> list[Discount]:
        return self._discounts[:]

    def total_price(self) -> float:
        """
        Calculates the total price of the receipt, including discounts.

        Returns:
            float: The total price of the receipt, rounded to 2 decimal places.
        """
        # Calculate the total price of all items on the receipt
        total_price = sum(item.total_price for item in self.items)

        # Calculate the total amount of all discounts applied to the receipt
        total_discounts = sum(discount.discount_amount for discount in self.discounts)

        # Calculate the total price by adding the total price of items and discounts
        total = total_price + total_discounts

        # Round the total price to 2 decimal places for display purposes
        return round(total, 2)

    def add_product(
        self, product: Product, quantity: float, price: float, total_price: float
    ) -> None:
        """
        Adds a product to the receipt.

        Args:
            product: The product being purchased.
            quantity: The quantity of the product being purchased.
            price: The price of a single unit of the product.
            total_price: The total price of the product (quantity * price).
        """
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, discount: Discount) -> None:
        """
        Adds a discount to the receipt.

        Args:
            discount: The discount to apply.
        """
        self._discounts.append(discount)
