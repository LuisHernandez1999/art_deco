from decimal import Decimal

from django.db import transaction

from shop.infrastructure.mappers.order_items import to_order_item_model, to_order_line
from shop.infrastructure.mappers.orders import (
    to_order_confirmation,
    to_order_model,
    to_order_receipt,
)
from shop.models import Order, OrderItem, Product


class DjangoOrderRepository:
    @transaction.atomic
    def place_order(self, *, customer_name, phone, address, city, notes, payment_method, lines):
        product_ids = {line.product_id for line in lines}
        products = {
            product.pk: product
            for product in Product.objects.filter(is_active=True, pk__in=product_ids)
        }
        if len(products) != len(product_ids):
            raise ValueError("Um dos itens não está mais disponível. Atualize seu carrinho.")

        order_lines = [to_order_line(products[line.product_id], line) for line in lines]
        total = sum(
            (line.total for line in order_lines if line.total is not None),
            Decimal("0.00"),
        )
        order = to_order_model(
            customer_name=customer_name,
            phone=phone,
            address=address,
            city=city,
            notes=notes,
            payment_method=payment_method,
            total=total,
        )
        order.save()
        OrderItem.objects.bulk_create([
            to_order_item_model(order, products[line.product_id], line)
            for line in order_lines
        ])
        return to_order_receipt(order)

    def get_order(self, reference):
        order = Order.objects.filter(reference=reference).first()
        if order is None:
            return None
        return to_order_confirmation(order)
