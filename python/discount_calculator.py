from typing import Optional, Callable

from model_objects import OfferType, Product, Discount, Offer


class DiscountCalculator:
    """
    Class to calculate discounts based on the offer type.
    """

    def __init__(
        self, product: Product, quantity: float, unit_price: float, offer: Offer
    ):
        """
        Initialize a new DiscountCalculator instance.

        Args:
            product (Product): The product for which to calculate the discount.
            quantity (float): The quantity of the product.
            unit_price (float): The unit price of the product.
            offer (Offer): The offer that specifies the discount type and argument.

        Raises:
            ValueError: If the quantity is less than or equal to zero or the unit price is negative.
        """
        if quantity <= 0 or unit_price < 0:
            raise ValueError(
                "Quantity must be positive and unit price cannot be negative."
            )

        self.product: Product = product
        self.quantity: int = int(quantity)
        self.unit_price: float = unit_price
        self.offer: Offer = offer

    def calculate_discount(self) -> Optional[Discount]:
        """
        Calculate the discount based on the offer type.

        Returns:
            Optional[Discount]: The calculated discount, or None if the offer type is unknown.

        Raises:
            ValueError: If the offer type is unknown.
        """
        discount_methods: dict[OfferType, Callable[[], Optional[Discount]]] = {
            OfferType.THREE_FOR_TWO: self.three_for_two_discount,
            OfferType.TWO_FOR_AMOUNT: self.two_for_amount_discount,
            OfferType.FIVE_FOR_AMOUNT: self.five_for_amount_discount,
            OfferType.TEN_PERCENT_DISCOUNT: self.ten_percent_discount,
        }

        if self.offer.offer_type in discount_methods:
            return discount_methods[self.offer.offer_type]()
        raise ValueError(f"Unknown offer type: {self.offer.offer_type}")

    def three_for_two_discount(self) -> Optional[Discount]:
        """
        Calculate the discount for the "three for two" offer.

        Returns:
            Optional[Discount]: The calculated discount, or None if the quantity is less than three.
        """
        return self.calculate_group_discount(
            self.product, self.quantity, self.unit_price, 3, 2 * self.unit_price
        )

    @staticmethod
    def calculate_group_discount(
        product: Product,
        quantity: int,
        unit_price: float,
        group_size: int,
        amount: float,
    ) -> Optional[Discount]:
        """
        Calculate the discount for a group discount offer.

        Args:
            product (Product): The product for which to calculate the discount.
            quantity (int): The quantity of the product.
            unit_price (float): The unit price of the product.
            group_size (int): The group size for the offer.
            amount (float): The amount for the offer.

        Returns:
            Optional[Discount]: The calculated discount, or None if the quantity is less than the group size.
        """
        if quantity >= group_size:
            number_of_groups = quantity // group_size
            total = amount * number_of_groups + (quantity % group_size) * unit_price
            discount_amount = quantity * unit_price - total
            return Discount(product, f"{group_size} for {amount}", -discount_amount)

    def two_for_amount_discount(self) -> Optional[Discount]:
        """
        Calculate the discount for the "two for amount" offer.

        Returns:
            Optional[Discount]: The calculated discount, or None if the quantity is less than two.
        """
        return self.amount_discount(
            self.product, self.quantity, self.unit_price, 2, self.offer.argument
        )

    def five_for_amount_discount(self) -> Optional[Discount]:
        """
        Calculate the discount for the "five for amount" offer.

        Returns:
            Optional[Discount]: The calculated discount, or None if the quantity is less than five.
        """
        return self.amount_discount(
            self.product, self.quantity, self.unit_price, 5, self.offer.argument
        )

    @staticmethod
    def amount_discount(
        product: Product,
        quantity: int,
        unit_price: float,
        group_size: int,
        amount: float,
    ) -> Optional[Discount]:
        """
        Calculate the discount amount for a group discount offer.

        Args:
            product (Product): The product for which to calculate the discount.
            quantity (int): The quantity of the product.
            unit_price (float): The unit price of the product.
            group_size (int): The group size for the offer.
            amount (float): The amount for the offer.

        Returns:
            Optional[Discount]: The calculated discount, or None if the quantity is less than the group size.
        """
        # Check if the quantity is sufficient to apply the group discount
        if quantity >= group_size:
            # Calculate the number of groups that can be formed
            number_of_groups = quantity // group_size
            # Calculate the total price after applying the group discount
            total = amount * number_of_groups + (quantity % group_size) * unit_price
            # Calculate the discount amount
            discount_amount = quantity * unit_price - total
            # Return the calculated discount
            return Discount(product, f"{group_size} for {amount}", -discount_amount)
        # If the quantity is less than the group size, return None
        return None

    def ten_percent_discount(self) -> Optional[Discount]:
        """
        Calculate the discount amount for a 10% discount offer.

        Returns:
            Optional[Discount]: The calculated discount.
        """
        # Check if the discount percentage is within the valid range
        if not (0 <= self.offer.argument <= 100):
            # Raise an error if the discount percentage is invalid
            raise ValueError("Discount percentage must be between 0 and 100.")
        # Calculate the discount amount
        discount_amount = (
            -self.quantity * self.unit_price * (self.offer.argument / 100.0)
        )
        # Return the calculated discount
        return Discount(self.product, f"{self.offer.argument}% off", discount_amount)
