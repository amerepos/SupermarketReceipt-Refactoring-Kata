from datetime import datetime
from io import StringIO

from model_objects import ProductUnit
from receipt import Receipt


class ReceiptPrinter:
    """
    A class responsible for printing receipts.

    Attributes:
        columns (int): The number of columns in the receipt.
    """

    def __init__(self, columns: int = 40):
        """
        Initializes a new ReceiptPrinter.

        Args:
            columns (int, optional): The number of columns in the receipt. Defaults to 40.
        """
        self.columns = columns

    def print_receipt(self, receipt: Receipt):
        """
        Prints a receipt.

        Args:
            receipt: The receipt to print.

        Returns:
            str: The printed receipt.
        """
        result = StringIO()
        # Print header
        result.write(self.format_line_with_whitespace("Supermarket Receipt", ""))
        result.write(
            self.format_line_with_whitespace(
                "Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        result.write("\n")
        # Print items
        for item in receipt.items:
            result.write(self.print_receipt_item(item))
        # Print discounts
        for discount in receipt.discounts:
            result.write(self.print_discount(discount))
        result.write("\n")
        result.write(self.present_total(receipt))
        # Print footer
        result.write("\n")
        result.write(self.format_line_with_whitespace("Thank you for shopping!", ""))
        result.write(self.format_line_with_whitespace("Please come back soon!", ""))
        return str(result.getvalue())

    def print_receipt_item(self, item):
        """
        Prints a receipt item.

        Args:
            item: The item to print.

        Returns:
            str: The printed item.
        """
        line = self.format_line_with_whitespace(
            item.product.name, self.print_price(item.total_price)
        )
        # If the quantity is not 1, print the price and quantity
        if item.quantity != 1:
            line += f"  {self.print_price(item.price)} * {self.print_quantity(item)}\n"
        return line

    def format_line_with_whitespace(self, name, value):
        """
        Formats a line with whitespace.

        Args:
            name (str): The name.
            value (str): The value.

        Returns:
            str: The formatted line.
        """
        # Calculate the number of whitespace characters needed
        total_length = len(name) + len(value)
        if total_length >= self.columns:
            # If the line is too long, truncate the name
            return f"{name[:self.columns - len(value) - 3]}...{value}\n"
        whitespace_size = self.columns - total_length
        return f"{name}{' ' * whitespace_size}{value}\n"

    @staticmethod
    def print_price(price):
        """
        Prints a price.

        Args:
            price (float): The price.

        Returns:
            str: The printed price.
        """
        # Format the price to 2 decimal places
        return f"{price:.2f}"

    @staticmethod
    def print_quantity(item):
        """
        Prints a quantity.

        Args:
            item: The item.

        Returns:
            str: The printed quantity.
        """
        # If the unit is EACH, print the quantity as an integer
        if ProductUnit.EACH == item.product.unit:
            return str(item.quantity)
        # Otherwise, print the quantity to 3 decimal places
        else:
            return f"{item.quantity:.3f}"

    def print_discount(self, discount):
        """
        Prints a discount.

        Args:
            discount: The discount.

        Returns:
            str: The printed discount.
        """
        return self.format_line_with_whitespace(
            f"{discount.description} ({discount.product.name})",
            self.print_price(discount.discount_amount),
        )

    def present_total(self, receipt):
        """
        Presents the total.

        Args:
            receipt: The receipt.

        Returns:
            str: The presented total.
        """
        return self.format_line_with_whitespace(
            "Total: ", self.print_price(receipt.total_price())
        )
