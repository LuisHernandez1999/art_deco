from dataclasses import dataclass
from decimal import Decimal

from .catalog import Product


@dataclass(frozen=True)
class CartLine:
    product: Product
    quantity: int
    line_total: Decimal | None


@dataclass(frozen=True)
class CartSummary:
    lines: tuple[CartLine, ...]
    total: Decimal
    quote_needed: bool
