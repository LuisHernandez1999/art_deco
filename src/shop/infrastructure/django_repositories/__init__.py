"""Compatibility exports for the original Django repository module path."""

from shop.infrastructure.repositories import (
    DjangoCatalogRepository,
    DjangoOrderRepository,
    DjangoSiteContentRepository,
)

__all__ = ["DjangoCatalogRepository", "DjangoOrderRepository", "DjangoSiteContentRepository"]
