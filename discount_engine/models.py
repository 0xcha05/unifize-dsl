from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Optional, Dict


class BrandTier(Enum):
    PREMIUM = "premium"
    REGULAR = "regular"
    BUDGET = "budget"


@dataclass
class Product:
    id: str
    brand: str
    brand_tier: BrandTier
    category: str
    base_price: Decimal
    current_price: Decimal


@dataclass
class CartItem:
    product: Product
    quantity: int
    size: str


@dataclass
class PaymentInfo:
    method: str
    bank_name: Optional[str]
    card_type: Optional[str]


@dataclass
class CustomerProfile:
    id: str
    name: str
    tier: str


@dataclass
class DiscountedPrice:
    original_price: Decimal
    final_price: Decimal
    applied_discounts: Dict[str, Decimal]
    message: str
