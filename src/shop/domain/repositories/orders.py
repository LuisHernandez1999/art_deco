from typing import Protocol
from uuid import UUID

from shop.domain.entities.orders import OrderConfirmation, OrderLineRequest, OrderReceipt, PaymentMethod


class OrderRepository(Protocol):
    def place_order(
        self,
        *,
        customer_name: str,
        phone: str,
        address: str,
        city: str,
        notes: str,
        payment_method: PaymentMethod,
        lines: list[OrderLineRequest],
    ) -> OrderReceipt: ...

    def get_order(self, reference: UUID) -> OrderConfirmation | None: ...
