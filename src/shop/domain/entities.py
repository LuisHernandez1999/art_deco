from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from uuid import UUID


class PaymentMethod(StrEnum):
    PIX = "pix"
    CARD = "card"
    CASH = "cash"


@dataclass(frozen=True)
class Product:
    id: int
    slug: str
    name: str
    category: str
    summary: str
    description: str
    price_from: Decimal | None
    image_url: str
    image_alt: str
    featured: bool

    @property
    def requires_quote(self) -> bool:
        return self.price_from is None


@dataclass(frozen=True)
class CatalogPage:
    items: tuple[Product, ...]
    number: int
    num_pages: int
    count: int
    has_next: bool
    has_previous: bool
    next_page: int | None
    previous_page: int | None


@dataclass(frozen=True)
class CarouselSlide:
    id: int
    page: str
    eyebrow: str
    title: str
    accent: str
    copy: str
    image_url: str
    image_alt: str
    button_label: str
    button_url: str


@dataclass(frozen=True)
class OrderLineRequest:
    product_id: int
    quantity: int


@dataclass(frozen=True)
class OrderReceipt:
    reference: UUID
    total: Decimal