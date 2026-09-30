from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID


class PaymentMethod(StrEnum):
    PIX = "pix"
    CARD = "card"
    CASH = "cash"


@dataclass(frozen=True)
class OrderLineRequest:
    product_id: int
    quantity: int


@dataclass(frozen=True)
class OrderLine:
    product_id: int
    product_name: str
    quantity: int
    unit_price: Decimal | None

    @property
    def requires_quote(self) -> bool:
        return self.unit_price is None

    @property
    def total(self) -> Decimal | None:
        if self.unit_price is None:
            return None
        return self.unit_price * self.quantity


@dataclass(frozen=True)
class OrderReceipt:
    reference: UUID
    total: Decimal


@dataclass(frozen=True)
class OrderConfirmation:
    reference: UUID
    customer_name: str
    created_at: datetime
    payment_method: str
    payment_method_display: str
