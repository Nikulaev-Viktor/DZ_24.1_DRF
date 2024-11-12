import stripe
from django.core.exceptions import ValidationError

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """Создание продукта в Stripe."""
    product_name = getattr(product, 'paid_course', None) or getattr(product, 'paid_lesson', None)

    if not product_name:
        raise ValidationError("Объект product должен иметь либо атрибут 'paid_course', либо 'paid_lesson'.")

    stripe_product = stripe.Product.create(name=str(product_name))
    product_id = stripe_product.get('id')
    return product_id


def create_stripe_price(amount, product_id):
    """Создание цены в Stripe"""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product=product_id,
    )
    price_id = price.get('id')
    return price_id


def create_stripe_session(price_id):
    """Создание сессии в Stripe"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    session_id = session.get('id')
    session_url = session.get('url')
    return session_id, session_url
