# Discount Engine

This engine applies discounts to shopping carts based on rules written in a simple DSL. You don’t need to touch Python code to add or change discount logic — just update the `rules/discounts.dsl` file.

## Assumptions & Design

- Rules are evaluated in order of `priority`. Lower values run first.
- You can stop evaluation early using `exclusive: true` in a rule.
- Conditions are evaluated against each cart item when needed (e.g. brand/category).
- Discounts are applied to the current price, one after another.

## Rule Structure

Each rule follows this basic format:
```dsl
rule "Unique Rule Name" {
    priority: <number>         # Lower number = higher priority
    exclusive: true|false      # If true, no other rule will run after this
    scope: cart|item           # 'cart' (default) or 'item'
    code: "OPTIONALCODE123"    # Optional. If provided, rule is only applied when this code is used

    when: <logical expression> # Condition under which rule is applied

    then:
        discount.percent: <number>    # Discount percentage (e.g., 10 for 10%)
        discount.name: "Label Name"   # Name shown in discount summary
}
```
All fields except priority, when, and then: block are optional.

## Variables You Can Use in `when`

You can write expressions using these variables:

| Variable         | Description                      |
| ---------------- | -------------------------------- |
| `cart_total`     | Total price of the cart          |
| `item_brand`     | Product brand                    |
| `item_category`  | Product category                 |
| `item_size`      | Size of the product              |
| `payment_method` | CARD, UPI, etc                   |
| `payment_bank`   | Bank name (for cards)            |
| `customer_tier`  | Loyalty tier (GOLD, SILVER, etc) |

## Logical Expressions

You can use Python-style logic in conditions:

```dsl
when: cart_total > 2000 and payment_method == "CARD"
when: item_brand == "PUMA" or customer_tier == "GOLD"
when: not item_size == "S"
```

Type of Rule Priority Range
Voucher 1–9
Item-level 10–49
Cart-level 50–99
Payment-based 100–149
Other fallback 150+

## run
fake data and a testcase is already configured:
```bash
python3 main.py
```