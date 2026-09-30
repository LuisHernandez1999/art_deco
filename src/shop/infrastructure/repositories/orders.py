from decimal import Decimal

from django.db import transaction

from shop.domain.entities.orders import OrderConfirmation, OrderReceipt
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

        order_lines = []
        total = Decimal("0.00")
        for line in lines:
            product = products[line.product_id]
            unit_price = product.price_from
            if unit_price is not None:
                total += unit_price * line.quantity
            order_lines.append((product, line.quantity, unit_price))

        order = Order.objects.create(
            customer_name=customer_name,
            phone=phone,
            address=address,
            city=city,
            notes=notes,
            payment_method=payment_method.value,
            total=total,
        )
        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                product=product,
                product_name=product.name,
                quantity=quantity,
                unit_price=unit_price,
                requires_quote=unit_price is None,
            )
            for product, quantity, unit_price in order_lines
        ])
        return OrderReceipt(reference=order.reference, total=total)

    def get_order(self, reference):
        order = Order.objects.filter(reference=reference).first()
        if order is None:
            return None
        return OrderConfirmation(
            reference=order.reference,
            customer_name=order.customer_name,
            created_at=order.created_at,
            payment_method=order.payment_method,
            payment_method_display=order.get_payment_method_display(),
        )
