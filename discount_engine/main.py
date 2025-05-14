import asyncio
from services.discount_service import DiscountService
from fake_data import cart_items, customer, payment_info


async def main():
    service = DiscountService()
    code = "SUPER69"
    result = await service.calculate_cart_discounts(
        cart_items=cart_items, customer=customer, payment_info=payment_info, code=code
    )
    print("Original Price:", result.original_price)
    print("Final Price:", result.final_price)
    print("Applied Discounts:", result.applied_discounts)
    print("Message:", result.message)


if __name__ == "__main__":
    asyncio.run(main())
