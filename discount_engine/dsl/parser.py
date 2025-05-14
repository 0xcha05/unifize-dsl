import re
import ast

from dsl.types import DSLRule
from dsl.validator import DSLRuleValidator
from dsl.logger import logger


class DSLParser:
    def __init__(self, file_path):
        with open(file_path, "r") as f:
            self.dsl = f.read()

    def _extract_line(self, text, key, fallback=None):
        pattern = f"{key}\\s*(.*?)\\n"
        match = re.search(pattern, text)
        return match.group(1).strip() if match else fallback

    def parse(self):
        rule_blocks = re.findall(r'rule\s+"(.*?)"\s*\{(.*?)\}', self.dsl, re.DOTALL)
        rules = []

        for name, body in rule_blocks:
            condition = self._extract_line(body, "when:")
            then = re.findall(r"discount\.(.*?):\s*(.*?)\n", body)
            actions = {k.strip(): ast.literal_eval(v.strip()) for k, v in then}
            priority = int(self._extract_line(body, "priority:", fallback="100"))
            exclusive = (
                self._extract_line(body, "exclusive:", fallback="false").lower()
                == "true"
            )
            scope = self._extract_line(body, "scope:", fallback="cart")
            code = self._extract_line(body, "code:", fallback=None)

            rule = DSLRule(name, condition, actions, priority, exclusive, scope, code)

            if DSLRuleValidator.validate(rule):
                rules.append(rule)
            else:
                logger.warning(f"Skipping invalid rule: {name}")

        return rules

    def _extract_line(self, body: str, keyword: str, fallback: str = "") -> str:
        match = re.search(rf"{keyword}\s*(.*?)\n", body)
        return match.group(1).strip() if match else fallback
