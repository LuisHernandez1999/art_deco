from typing import Protocol

from shop.domain.entities.site_content import CarouselSlide


class SiteContentRepository(Protocol):
    def list_carousel(self, page: str) -> list[CarouselSlide]: ...
