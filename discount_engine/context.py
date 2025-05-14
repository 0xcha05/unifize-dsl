from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict
from models import CartItem, CustomerProfile, PaymentInfo


class DiscountContext:
    def __init__(
        self,
        cart: List[CartItem],
        customer: CustomerProfile,
        payment_info: PaymentInfo = None,
    ):
        self.cart = cart
        self.customer = customer
        self.payment_info = payment_info
        self.original_price = sum(
            item.product.base_price * item.quantity for item in cart
        )
        self.current_price = self.original_price
        self.discounts_applied: Dict[str, Decimal] = {}
        self.messages: List[str] = []

    def apply_discount(self, name: str, amount: Decimal):
        if amount > 0:
            rounded = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            self.current_price -= rounded
            self.discounts_applied[name] = rounded
            self.messages.append(f"{name}: -{rounded:.2f}")
