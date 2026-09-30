from decimal import Decimal

from shop.domain.entities.orders import (
    OrderConfirmation,
    OrderReceipt,
    PaymentMethod,
)
from shop.models import Order as OrderModel


def to_order_model(
    *,
    customer_name: str,
    phone: str,
    address: str,
    city: str,
    notes: str,
    payment_method: PaymentMethod,
    total: Decimal,
) -> OrderModel:
    return OrderModel(
        customer_name=customer_name,
        phone=phone,
        address=address,
        city=city,
        notes=notes,
        payment_method=payment_method.value,
        total=total,
    )
def to_order_receipt(model: OrderModel) -> OrderReceipt:
    return OrderReceipt(reference=model.reference, total=model.total)


def to_order_confirmation(model: OrderModel) -> OrderConfirmation:
    return OrderConfirmation(
        reference=model.reference,
        customer_name=model.customer_name,
        created_at=model.created_at,
        payment_method=model.payment_method,
        payment_method_display=model.get_payment_method_display(),
    )
