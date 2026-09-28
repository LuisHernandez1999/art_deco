from typing import Protocol
from uuid import UUID

from .entities import CarouselSlide, OrderLineRequest, OrderReceipt, PaymentMethod, Product


class CatalogRepository(Protocol):
    def list_active(self, category: str = "", query: str = "") -> list[Product]: ...

    def get_by_slug(self, slug: str) -> Product | None: ...

    def get_by_id(self, product_id: int) -> Product | None: ...


class OrderRepository(Protocol):
    def place_order(self, *, customer_name: str, phone: str, address: str, city: str,
                    notes: str, payment_method: PaymentMethod,
                    lines: list[OrderLineRequest]) -> OrderReceipt: ...

    def get_order(self, reference: UUID): ...


class SiteContentRepository(Protocol):
    def list_carousel(self, page: str) -> list[CarouselSlide]: ...