from dsl.types import DSLRule
from dsl.logger import logger


class DSLRuleValidator:
    REQUIRED_FIELDS = ["percent", "name"]

    @staticmethod
    def validate(rule: DSLRule) -> bool:
        errors = []

        if not rule.condition:
            errors.append("Missing 'when' condition")

        for field in DSLRuleValidator.REQUIRED_FIELDS:
            if field not in rule.actions:
                errors.append(f"Missing 'discount.{field}' in actions")

        if not isinstance(rule.actions.get("percent", 0), (int, float)):
            errors.append("discount.percent must be a number")

        if errors:
            logger.error(f"[Invalid Rule: {rule.name}] → {', '.join(errors)}")
            return False

        return True
