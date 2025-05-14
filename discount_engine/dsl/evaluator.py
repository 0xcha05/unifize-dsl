from decimal import Decimal
from context import DiscountContext


class DSLEvaluator:
    def __init__(self, rules):
        self.rules = sorted(rules, key=lambda r: r.priority)

    def evaluate(self, context: DiscountContext, code: str = None):
        matched_exclusive = None

        # First pass: find exclusive rule to apply (if any)
        for rule in self.rules:
            if rule.code and rule.code != code:
                continue  # skip non-matching voucher rules

            if rule.exclusive:
                if self._rule_matches(rule, context):
                    matched_exclusive = rule
                    break  # apply only this one rule

        # If an exclusive rule matched, apply just that
        if matched_exclusive:
            self._apply_rule(matched_exclusive, context)
            return

        # Otherwise, apply all non-exclusive matching rules
        for rule in self.rules:
            if rule.code and rule.code != code:
                continue

            if rule.exclusive:
                continue  # already handled in pass 1

            if self._rule_matches(rule, context):
                self._apply_rule(rule, context)

    def _rule_matches(self, rule, context):
        for item in context.cart:
            env = {
                "item_brand": item.product.brand,
                "item_category": item.product.category,
                "item_size": item.size,
                "customer_tier": context.customer.tier,
                "cart_total": float(context.original_price),
                "payment_method": getattr(context.payment_info, "method", None),
                "payment_bank": getattr(context.payment_info, "bank_name", None),
            }

            try:
                if eval(rule.condition, {}, env):
                    return True
            except Exception:
                continue
        return False

    def _apply_rule(self, rule, context):
        if rule.scope == "cart":
            # Evaluate just once at the cart level
            env = {
                "customer_tier": context.customer.tier,
                "cart_total": float(context.original_price),
                "payment_method": getattr(context.payment_info, "method", None),
                "payment_bank": getattr(context.payment_info, "bank_name", None),
            }

            try:
                if eval(rule.condition, {}, env):
                    amount = context.current_price * Decimal(
                        rule.actions["percent"] / 100
                    )
                    context.apply_discount(rule.actions["name"], amount)
            except Exception:
                pass
            return

        # Item-level scope
        for item in context.cart:
            env = {
                "item_brand": item.product.brand,
                "item_category": item.product.category,
                "item_size": item.size,
                "customer_tier": context.customer.tier,
                "cart_total": float(context.original_price),
                "payment_method": getattr(context.payment_info, "method", None),
                "payment_bank": getattr(context.payment_info, "bank_name", None),
            }

            try:
                if eval(rule.condition, {}, env):
                    base_price = item.product.base_price * item.quantity
                    amount = base_price * Decimal(rule.actions["percent"] / 100)
                    context.apply_discount(rule.actions["name"], amount)
            except Exception:
                continue

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
