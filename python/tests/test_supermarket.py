import math
from enum import Enum
from unittest.mock import Mock

import pytest

from discount_calculator import DiscountCalculator
from model_objects import Product, OfferType, ProductUnit, Offer, Discount
from receipt import ReceiptItem, Receipt
from receipt_printer import ReceiptPrinter
from shopping_cart import ShoppingCart
from teller import Teller

apple = Product(name="Apple", unit=ProductUnit.EACH)
banana = Product(name="Banana", unit=ProductUnit.EACH)
orange = Product(name="Orange", unit=ProductUnit.EACH)
grape = Product(name="Grapes", unit=ProductUnit.KILO)
pineapple = Product(name="Pineapple", unit=ProductUnit.EACH)
watermelon = Product(name="Watermelon", unit=ProductUnit.EACH)
strawberry = Product(name="Strawberry", unit=ProductUnit.EACH)
blueberry = Product(name="Blueberry", unit=ProductUnit.EACH)
mango = Product(name="Mango", unit=ProductUnit.EACH)
peach = Product(name="Peach", unit=ProductUnit.EACH)
diamond = Product(name="Diamond", unit=ProductUnit.EACH)
milk = Product(name="Milk", unit=ProductUnit.EACH)


class TestDiscountCalculator:
    """
    Test suite for the DiscountCalculator class.
    """

    # Calculate discount for "three for two" offer with sufficient quantity
    def test_three_for_two_discount_sufficient_quantity(self):
        """
        Test that the "three for two" offer is correctly calculated when the quantity is sufficient.
        """
        # Create an offer for the "three for two" discount
        offer = Offer(offer_type=OfferType.THREE_FOR_TWO, argument=0)

        # Create a DiscountCalculator instance with the offer and sufficient quantity
        calculator = DiscountCalculator(
            product=apple, quantity=3, unit_price=1.0, offer=offer
        )

        # Calculate the discount
        discount = calculator.calculate_discount()

        # Assert that the discount is not None and has the correct amount
        assert discount is not None
        assert discount.discount_amount == -1.0

    # Calculate discount for "two for amount" offer with sufficient quantity
    def test_two_for_amount_discount_sufficient_quantity(self):
        """
        Test that the "two for amount" offer is correctly calculated when the quantity is sufficient.
        """
        # Create an offer for the "two for amount" discount
        offer = Offer(offer_type=OfferType.TWO_FOR_AMOUNT, argument=1.5)

        # Create a DiscountCalculator instance with the offer and sufficient quantity
        calculator = DiscountCalculator(
            product=banana, quantity=2, unit_price=1.0, offer=offer
        )

        # Calculate the discount
        discount = calculator.calculate_discount()

        # Assert that the discount is not None and has the correct amount
        assert discount is not None
        assert discount.discount_amount == -0.5

    # Raise ValueError for negative unit price
    def test_negative_unit_price_raises_value_error(self):
        """
        Test that a ValueError is raised when the unit price is negative.
        """
        # Create an offer for a discount
        offer = Offer(offer_type=OfferType.TEN_PERCENT_DISCOUNT, argument=10)

        # Attempt to create a DiscountCalculator instance with a negative unit price
        with pytest.raises(ValueError, match="unit price cannot be negative"):
            DiscountCalculator(product=apple, quantity=1, unit_price=-1.0, offer=offer)

    # Raise ValueError for zero or negative quantity
    def test_zero_or_negative_quantity_raises_value_error(self):
        """
        Test that a ValueError is raised when the quantity is zero or negative.
        """
        # Create an offer for a discount
        offer = Offer(offer_type=OfferType.FIVE_FOR_AMOUNT, argument=5.0)

        # Attempt to create a DiscountCalculator instance with a zero quantity
        with pytest.raises(ValueError, match="Quantity must be positive"):
            DiscountCalculator(product=grape, quantity=0, unit_price=2.0, offer=offer)

        # Attempt to create a DiscountCalculator instance with a negative quantity
        with pytest.raises(ValueError, match="Quantity must be positive"):
            DiscountCalculator(product=grape, quantity=-1, unit_price=2.0, offer=offer)

    # Raise ValueError for unknown offer type
    def test_unknown_offer_type_raises_value_error(self):
        """
        Test that a ValueError is raised when the offer type is unknown.
        """

        # Create an unknown offer type
        class UnknownOfferType(Enum):
            UNKNOWN = 99

        # Create an offer with the unknown offer type
        offer = Offer(offer_type=UnknownOfferType.UNKNOWN, argument=0)

        # Create a DiscountCalculator instance with the unknown offer type
        calculator = DiscountCalculator(
            product=pineapple, quantity=1, unit_price=1.0, offer=offer
        )

        # Attempt to calculate the discount
        with pytest.raises(ValueError, match="Unknown offer type"):
            calculator.calculate_discount()


class TestReceiptItem:

    @pytest.fixture
    def setup_item(self):
        """Fixture to create a default ReceiptItem."""
        return ReceiptItem(apple, 2, 1.5, 3.0)

    # Creating a ReceiptItem with valid product, quantity, price, and total_price
    def test_create_receipt_item_with_valid_data(self):
        item = ReceiptItem(apple, 2, 1.5, 3.0)
        assert item.product == apple
        assert item.quantity == 2
        assert math.isclose(item.price, 1.5, rel_tol=1e-9)
        assert math.isclose(item.total_price, 3.0, rel_tol=1e-9)

    # Accessing attributes product, quantity, price, and total_price after initialization
    def test_access_attributes_after_initialization(self, setup_item):
        item = setup_item
        assert item.product == apple
        assert item.quantity == 2
        assert math.isclose(item.price, 1.5, rel_tol=1e-9)
        assert math.isclose(item.total_price, 3.0, rel_tol=1e-9)

    # Initializing multiple ReceiptItems and verifying their independence
    def test_multiple_receipt_items_independence(self):
        item1 = ReceiptItem(orange, 3, 1.0, 3.0)
        item2 = ReceiptItem(grape, 2, 2.0, 4.0)
        assert item1.product == orange
        assert item2.product == grape
        assert item1.total_price != item2.total_price

    # Initializing ReceiptItem with zero quantity
    def test_initialize_with_zero_quantity(self):
        item = ReceiptItem(watermelon, 0, 3.0, 0.0)
        assert item.quantity == 0
        assert math.isclose(item.total_price, 0.0, rel_tol=1e-9)

        # Initializing ReceiptItem with negative price
    def test_initialize_with_negative_price(self):
        item = ReceiptItem(pineapple, 1, -1.0, -1.0)
        assert math.isclose(item.price, -1.0, rel_tol=1e-9)
        assert math.isclose(item.total_price, -1.0, rel_tol=1e-9)

    # Initializing ReceiptItem with total_price not matching quantity * price
    def test_total_price_mismatch(self):
        item = ReceiptItem(mango, 2, 2.5, 6.0)
        assert item.total_price != item.quantity * item.price

    # Initializing ReceiptItem with empty product name

    # Verifying immutability of ReceiptItem attributes after initialization
    def test_immutability_of_attributes(self):
        item = ReceiptItem(strawberry, 10, 0.5, 5.0)
        with pytest.raises(AttributeError):
            item.product = blueberry  # Attempting to change the product name

    # Testing ReceiptItem with very large quantity and price values
    def test_large_quantity_and_price_values(self):
        large_quantity = 10**6
        large_price = 10**6
        total_price = large_quantity * large_price
        item = ReceiptItem(diamond, large_quantity, large_price, total_price)
        assert item.quantity == large_quantity
        assert math.isclose(item.price, large_price, rel_tol=1e-9)
        assert math.isclose(item.total_price, total_price, rel_tol=1e-9)


@pytest.mark.usefixtures("setup_supermarket")
class TestSupermarket:

    @pytest.fixture(autouse=True)
    def setup_supermarket(self):
        # Set up the mock catalog and other necessary components
        self.catalog = Mock()
        self.teller = Teller(self.catalog)
        self.the_cart = ShoppingCart()

        # Define products
        self.toothbrush = Product("toothbrush", ProductUnit.EACH)
        self.rice = Product("rice", ProductUnit.EACH)
        self.apples = Product("apples", ProductUnit.KILO)
        self.cherry_tomatoes = Product("cherry tomato box", ProductUnit.EACH)

        # Set up mock prices for products
        self.catalog.unit_price.side_effect = lambda product: {
            self.toothbrush: 0.99,
            self.rice: 2.99,
            self.apples: 1.99,
            self.cherry_tomatoes: 0.69,
        }[product]

    def test_an_empty_shopping_cart_should_cost_nothing(self):
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert math.isclose(receipt.total_price(), 0.0, rel_tol=1e-9)
        assert len(receipt.items) == 0

    def test_one_normal_item(self):
        self.the_cart.add_item(self.toothbrush)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert math.isclose(receipt.total_price(), 0.99, rel_tol=1e-9)
        assert len(receipt.items) == 1

    def test_two_normal_items(self):
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.rice)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert math.isclose(receipt.total_price(), 3.98, rel_tol=1e-9)
        assert len(receipt.items) == 2

    def test_buy_two_get_one_free(self):
        self.the_cart.add_item_quantity(self.toothbrush, 2)
        self.teller.add_special_offer(OfferType.THREE_FOR_TWO, self.toothbrush, 0.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert math.isclose(receipt.total_price(), 1.98, rel_tol=1e-9)

    def test_buy_five_get_one_free(self):
        self.the_cart.add_item_quantity(self.toothbrush, 5)
        self.teller.add_special_offer(OfferType.THREE_FOR_TWO, self.toothbrush, 0.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert math.isclose(receipt.total_price(), 3.96, rel_tol=1e-9)

    def test_loose_weight_product(self):
        self.the_cart.add_item_quantity(self.apples, 0.5)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert math.isclose(receipt.total_price(), 0.99, rel_tol=1e-9)

    def test_percent_discount(self):
        self.the_cart.add_item(self.rice)
        self.teller.add_special_offer(OfferType.TEN_PERCENT_DISCOUNT, self.rice, 10.0)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert math.isclose(receipt.total_price(), 2.69, rel_tol=1e-9)

    def test_x_for_y_discount(self):
        self.the_cart.add_item_quantity(self.cherry_tomatoes, 2)
        self.teller.add_special_offer(
            OfferType.TWO_FOR_AMOUNT, self.cherry_tomatoes, 0.99
        )
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert math.isclose(receipt.total_price(), 0.99, rel_tol=1e-9)

    def test_five_for_y_discount(self):
        self.the_cart.add_item_quantity(self.apples, 5)
        self.teller.add_special_offer(OfferType.FIVE_FOR_AMOUNT, self.apples, 5.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert math.isclose(receipt.total_price(), 5.99, rel_tol=1e-9)

    def test_five_for_y_discount_with_six(self):
        self.the_cart.add_item_quantity(self.apples, 6)
        self.teller.add_special_offer(OfferType.FIVE_FOR_AMOUNT, self.apples, 5.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert math.isclose(receipt.total_price(), 7.98, rel_tol=1e-9)

    def test_five_for_y_discount_with_sixteen(self):
        self.the_cart.add_item_quantity(self.apples, 16)
        self.teller.add_special_offer(OfferType.FIVE_FOR_AMOUNT, self.apples, 7.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert math.isclose(receipt.total_price(), 25.96, rel_tol=1e-9)

    def test_five_for_y_discount_with_four(self):
        self.the_cart.add_item_quantity(self.apples, 4)
        self.teller.add_special_offer(OfferType.FIVE_FOR_AMOUNT, self.apples, 6.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert math.isclose(receipt.total_price(), 7.96, rel_tol=1e-9)


class TestReceiptPrinter:

    # ReceiptPrinter initializes with default column width
    def test_initializes_with_default_column_width(self):
        printer = ReceiptPrinter()
        assert printer.columns == 40

    # ReceiptPrinter prints a receipt with header, items, discounts, and footer
    def test_prints_receipt_with_header_items_discounts_footer(self):

        receipt = Receipt()
        receipt.add_product(apple, 2, 1.5, 3.0)
        printer = ReceiptPrinter()
        output = printer.print_receipt(receipt)
        assert "Supermarket Receipt" in output
        assert "Thank you for shopping!" in output

    # ReceiptPrinter formats lines with whitespace correctly
    def test_formats_lines_with_whitespace_correctly(self):
        printer = ReceiptPrinter(columns=20)
        formatted_line = printer.format_line_with_whitespace("Name", "Value")
        assert formatted_line == "Name           Value\n"

    # ReceiptPrinter prints item prices formatted to two decimal places
    def test_prints_item_prices_formatted_to_two_decimal_places(self):
        price = 5.5
        formatted_price = ReceiptPrinter.print_price(price)
        assert formatted_price == "5.50"

    # ReceiptPrinter prints quantities correctly based on unit type
    def test_prints_quantities_correctly_based_on_unit_type(self):
        item = ReceiptItem(
            product=grape,
            quantity=1.234,
            price=1,
            total_price=1.234,
        )
        quantity_str = ReceiptPrinter.print_quantity(item)
        assert quantity_str == "1.234"

    # ReceiptPrinter handles receipts with no items or discounts
    def test_handles_receipts_with_no_items_or_discounts(self):
        receipt = Receipt()
        printer = ReceiptPrinter()
        output = printer.print_receipt(receipt)
        assert "Total:" in output

    # ReceiptPrinter handles zero quantity items
    def test_handles_zero_quantity_items(self):
        receipt = Receipt()
        receipt.add_product(product=banana, quantity=0, price=0.0, total_price=0.0)
        printer = ReceiptPrinter()
        output = printer.print_receipt(receipt)
        assert "Banana" in output and "0" in output

    # ReceiptPrinter handles negative discount amounts
    def test_handles_negative_discount_amounts(self):
        discount = Discount(product=milk, description="Discount", discount_amount=-1.5)
        receipt = Receipt()
        receipt.add_discount(discount)
        printer = ReceiptPrinter()
        output = printer.print_receipt(receipt)
        assert "Discount (Milk)" in output and "-1.50" in output

    # ReceiptPrinter handles very large total prices
    def test_handles_very_large_total_prices(self):
        receipt = Receipt()
        receipt.add_product(
            product=banana, quantity=1000000, price=0.99, total_price=1000000.99
        )
        printer = ReceiptPrinter()
        output = printer.print_receipt(receipt)
        assert "1000000.99" in output
