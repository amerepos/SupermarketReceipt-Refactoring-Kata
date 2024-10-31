from catalog import SupermarketCatalog
from model_objects import Offer, OfferType, Product
from receipt import Receipt
from shopping_cart import ShoppingCart


class Teller:
    """
    Represents a teller that can generate receipts for shopping carts.
    """

    def __init__(self, catalog: SupermarketCatalog):
        """
        Initializes a new instance of the Teller class.

        Args:
            catalog (SupermarketCatalog): The catalog of products and their prices.
        """
        self.catalog = catalog
        self.offers = {}

    def add_special_offer(
        self, offer_type: OfferType, product: Product, argument: float
    ):
        """
        Adds a special offer for a given product.

        Args:
            offer_type (OfferType): The type of special offer.
            product (Product): The product to add the special offer for.
            argument (float): The argument for the special offer.
        """
        self.offers[product] = Offer(offer_type, argument)

    def checks_out_articles_from(self, shopping_cart: ShoppingCart) -> Receipt:
        """
        Generates a receipt for all items in the shopping cart.

        Args:
            shopping_cart (ShoppingCart): The shopping cart to generate the receipt for.

        Returns:
            Receipt: The generated receipt.
        """
        # Create a new receipt
        receipt = Receipt()

        # Add cart items to the receipt
        self._add_cart_items_to_receipt(shopping_cart, receipt)

        # Apply any relevant offers to the receipt
        self._apply_offers(shopping_cart, receipt)

        # Return the generated receipt
        return receipt

    def _add_cart_items_to_receipt(self, shopping_cart: ShoppingCart, receipt: Receipt):
        """
        Adds each item from the shopping cart to the receipt.

        Args:
            shopping_cart (ShoppingCart): The shopping cart to add items from.
            receipt (Receipt): The receipt to add items to.
        """
        for item in shopping_cart.items:
            # Process the item and add it to the receipt
            self._process_item(item.product, item.quantity, receipt)

    def _process_item(self, product: Product, quantity: int, receipt: Receipt):
        """
        Calculates total price for an item and adds it to the receipt.

        Args:
            product (Product): The product to process.
            quantity (int): The quantity of the product.
            receipt (Receipt): The receipt to add the item to.
        """
        # Get the unit price of the product from the catalog
        unit_price = self.catalog.unit_price(product)

        # Calculate the total price for the item
        total_price = self._calculate_total_price(quantity, unit_price)

        # Add the item to the receipt
        receipt.add_product(product, quantity, unit_price, total_price)

    def _apply_offers(self, shopping_cart: ShoppingCart, receipt: Receipt):
        """
        Applies any relevant offers from the shopping cart to the receipt.

        Args:
            shopping_cart (ShoppingCart): The shopping cart to apply offers from.
            receipt (Receipt): The receipt to apply offers to.
        """
        shopping_cart.handle_offers(receipt, self.offers, self.catalog)

    @staticmethod
    def _calculate_total_price(quantity: int, unit_price: float) -> float:
        """
        Calculates total price based on quantity and unit price.

        Args:
            quantity (int): The quantity of the item.
            unit_price (float): The unit price of the item.

        Returns:
            float: The total price.
        """
        return quantity * unit_price
