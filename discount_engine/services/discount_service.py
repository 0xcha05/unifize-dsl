from decimal import Decimal, ROUND_HALF_UP

from dsl.parser import DSLParser
from dsl.evaluator import DSLEvaluator
from context import DiscountContext
from models import DiscountedPrice


class DiscountService:
    def __init__(self):
        rules = DSLParser("rules/discounts.dsl").parse()
        self.evaluator = DSLEvaluator(rules)

    async def calculate_cart_discounts(
        self, cart_items, customer, payment_info=None, code=None
    ):
        context = DiscountContext(cart_items, customer, payment_info)
        self.evaluator.evaluate(context, code)
        return DiscountedPrice(
            original_price=context.original_price.quantize(Decimal("0.01")),
            final_price=context.current_price.quantize(Decimal("0.01")),
            applied_discounts=context.discounts_applied,
            message="; ".join(context.messages),
        )

    async def validate_discount_code(self, code: str, cart_items, customer) -> bool:
        return self.evaluator.validate_code(code, cart_items, customer)
