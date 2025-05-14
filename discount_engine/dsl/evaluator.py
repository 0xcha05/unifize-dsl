from decimal import Decimal
from context import DiscountContext


class DSLEvaluator:
    def __init__(self, rules):
        self.rules = sorted(rules, key=lambda r: r.priority)

    def evaluate(self, context: DiscountContext, code: str = None):
        for rule in self.rules:
            if rule.code and rule.code != code:
                continue  # voucher mismatch

            if rule.scope == "item":
                for item in context.cart:
                    env = {
                        "item.brand": item.product.brand,
                        "item.category": item.product.category,
                        "item.size": item.size,
                    }
                    try:
                        if eval(rule.condition, {}, env):
                            base_price = item.product.base_price * item.quantity
                            amount = base_price * Decimal(rule.actions["percent"] / 100)
                            context.apply_discount(rule.actions["name"], amount)
                            if rule.exclusive:
                                return
                    except:
                        continue
            else:
                if self._evaluate_condition(rule.condition, context):
                    amount = context.current_price * Decimal(
                        rule.actions["percent"] / 100
                    )
                    context.apply_discount(rule.actions["name"], amount)
                    if rule.exclusive:
                        return

    def _evaluate_condition(self, expr: str, context: DiscountContext) -> bool:
        base_env = {
            "cart_total": float(context.original_price),
            "customer_tier": context.customer.tier,
            "payment_method": getattr(context.payment_info, "method", None),
            "payment_bank": getattr(context.payment_info, "bank_name", None),
        }

        for item in context.cart:
            item_env = base_env.copy()
            item_env.update(
                {
                    "item_brand": item.product.brand,
                    "item_category": item.product.category,
                    "item_size": item.size,
                }
            )

            try:
                if eval(expr, {}, item_env):
                    return True
            except Exception:
                continue

        return False

    def validate_code(self, code: str, cart, customer) -> bool:
        for rule in self.rules:
            if rule.code != code:
                continue
            context = DiscountContext(cart, customer)
            return self._evaluate_condition(rule.condition, context)
        return False
