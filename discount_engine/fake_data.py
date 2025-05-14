from models import *
from decimal import Decimal

puma_tshirt = Product(
    id="t1",
    brand="PUMA",
    brand_tier=BrandTier.REGULAR,
    category="T-shirt",
    base_price=Decimal("1000"),
    current_price=Decimal("1000"),
)

cart_items = [CartItem(product=puma_tshirt, quantity=3, size="M")]  # 3000

payment_info = PaymentInfo(method="CARD", bank_name="ICICI", card_type="CREDIT")

customer = CustomerProfile(id="123", name="John", tier="GOLD")
