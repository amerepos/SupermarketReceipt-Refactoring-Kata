from typing import Dict

from discount_calculator import DiscountCalculator
from catalog import SupermarketCatalog
from model_objects import ProductQuantity, Product, Offer
from receipt import Receipt


class ShoppingCart:
    """
    Represents a shopping cart that can hold products and calculate discounts.
    """

    def __init__(self):
        """
        Initializes a new instance of the ShoppingCart class.
        """
        # Initialize an empty list to store product quantities
        self._items: list[ProductQuantity] = []
        # Initialize an empty dictionary to store product quantities
        self._product_quantities: Dict[Product, float] = {}

    @property
    def items(self) -> list[ProductQuantity]:
        """
        Gets the list of product quantities in the shopping cart.

        Returns:
            list[ProductQuantity]: The list of product quantities.
        """
        return self._items

    def add_item(self, product: Product) -> None:
        """
        Adds a product to the shopping cart with a quantity of 1.

        Args:
            product (Product): The product to add.
        """
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self) -> Dict[Product, float]:
        """
        Gets the dictionary of product quantities in the shopping cart.

        Returns:
            Dict[Product, float]: The dictionary of product quantities.
        """
        return self._product_quantities

    def add_item_quantity(self, product: Product, quantity: float) -> None:
        """
        Adds a product to the shopping cart with a specified quantity.

        Args:
            product (Product): The product to add.
            quantity (float): The quantity of the product.
        """
        # Create a new ProductQuantity instance and add it to the list
        self._items.append(ProductQuantity(product, quantity))
        # Get the existing quantity or 0 if it doesn't exist and add the quantity
        self._product_quantities[product] = (
            self._product_quantities.get(product, 0) + quantity
        )

    def handle_offers(
        self,
        receipt: Receipt,
        offers: Dict[Product, Offer],
        catalog: SupermarketCatalog,
    ) -> None:
        """
        Applies offers to the products in the shopping cart and updates the receipt.

        Args:
            receipt (Receipt): The receipt to update.
            offers (Dict[Product, Offer]): The offers to apply.
            catalog (SupermarketCatalog): The catalog of products and prices.
        """
        # Iterate over the products and quantities in the shopping cart
        for product, quantity in self._product_quantities.items():
            # Check if the product has an offer
            if product not in offers:
                continue  # Skip if the product is not in offers

            # Get the offer for the product
            offer = offers[product]
            # Get the unit price of the product from the catalog
            unit_price = catalog.unit_price(product)

            # Create a discount calculator and calculate the discount
            discount_calculator = DiscountCalculator(
                product, quantity, unit_price, offer
            )
            discount = discount_calculator.calculate_discount()

            # Add the discount to the receipt if it exists
            if discount:
                receipt.add_discount(discount)
