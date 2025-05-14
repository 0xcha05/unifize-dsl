rule "GOLD Exclusive Voucher" {
    priority: 1
    exclusive: false
    when: customer_tier == "GOLD"
    then:
        discount.percent: 50
        discount.name: "GOLD Voucher"
}

rule "PUMA Brand Discount" {
    priority: 10
    when: item_brand == "PUMA"
    then:
        discount.percent: 40
        discount.name: "PUMA Discount"
}

rule "Cart Over 2000" {
    priority: 100
    when: cart_total > 2000
    then:
        discount.percent: 10
        discount.name: "Cart Value Discount"
}

rule "ICICI Card Offer" {
    priority: 200
    when: payment_method == "CARD" and payment_bank == "ICICI"
    then:
        discount.percent: 10
        discount.name: "ICICI Bank Offer"
}

rule "Broken Rule" {
    priority: 300
    when: customer_tier == "GOLD"
    then:
        discount.name: "This Will Break"
        discount.percent: "fifty"  # not a number
}
