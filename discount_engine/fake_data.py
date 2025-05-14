from models import *
from decimal import Decimal

# Existing product
puma_tshirt = Product(
    id="t1",
    brand="PUMA",
    brand_tier=BrandTier.REGULAR,
    category="T-shirt",
    base_price=Decimal("1000"),
    current_price=Decimal("1000"),
)

# Additional products
nike_shoes = Product(
    id="s1",
    brand="NIKE",
    brand_tier=BrandTier.PREMIUM,
    category="Shoes",
    base_price=Decimal("5000"),
    current_price=Decimal("4500"),
)

adidas_jacket = Product(
    id="j1",
    brand="ADIDAS",
    brand_tier=BrandTier.REGULAR,
    category="Jacket",
    base_price=Decimal("3000"),
    current_price=Decimal("2800"),
)

uniqlo_jeans = Product(
    id="je1",
    brand="UNIQLO",
    brand_tier=BrandTier.BUDGET,
    category="Jeans",
    base_price=Decimal("2000"),
    current_price=Decimal("1800"),
)

zara_dress = Product(
    id="d1",
    brand="ZARA",
    brand_tier=BrandTier.PREMIUM,
    category="Dress",
    base_price=Decimal("3500"),
    current_price=Decimal("3150"),
)

# Cart items
cart_items = [
    CartItem(product=puma_tshirt, quantity=3, size="M"),  # 3000
    CartItem(product=nike_shoes, quantity=1, size="10"),  # 4500
    CartItem(product=adidas_jacket, quantity=2, size="L"),  # 5600
    CartItem(product=uniqlo_jeans, quantity=1, size="32"),  # 1800
    CartItem(product=zara_dress, quantity=1, size="S"),  # 3150
]

# Payment info
payment_info = PaymentInfo(method="CARD", bank_name="ICICI", card_type="CREDIT")

# Customer profile
customer = CustomerProfile(id="123", name="John", tier="GOLD")
