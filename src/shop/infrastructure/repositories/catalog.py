from django.core.paginator import Paginator
from django.db.models import Q

from shop.domain.entities.catalog import CatalogPage
from shop.infrastructure.mappers.product import to_product
from shop.models import Product as ProductModel


class DjangoCatalogRepository:
    def _queryset(self, category="", query="", exclude_slug=""):
        products = ProductModel.objects.filter(is_active=True)
        if category:
            products = products.filter(category=category)
        if query:
            products = products.filter(Q(name__icontains=query) | Q(summary__icontains=query))
        if exclude_slug:
            products = products.exclude(slug=exclude_slug)
        return products.only(
            "id", "slug", "name", "category", "summary", "description",
            "price_from", "image_url", "image_alt", "featured",
        ).order_by("-featured", "name", "pk")

    def list_active(self, category="", query="", exclude_slug="", limit=None):
        products = self._queryset(category, query, exclude_slug)
        if limit is not None:
            products = products[:limit]
        return [to_product(product) for product in products]

    def list_active_page(self, *, category="", query="", page_number=1, per_page=6):
        paginator = Paginator(self._queryset(category, query), per_page)
        page = paginator.get_page(page_number)
        return CatalogPage(
            items=tuple(to_product(product) for product in page.object_list),
            number=page.number,
            num_pages=paginator.num_pages,
            count=paginator.count,
            has_next=page.has_next(),
            has_previous=page.has_previous(),
            next_page=page.next_page_number() if page.has_next() else None,
            previous_page=page.previous_page_number() if page.has_previous() else None,
        )

    def list_categories(self):
        return list(ProductModel.Category.choices)

    def get_by_slug(self, slug):
        product = self._queryset().filter(slug=slug).first()
        return to_product(product) if product else None

    def get_by_id(self, product_id):
        product = self._queryset().filter(pk=product_id).first()
        return to_product(product) if product else None

    def get_by_ids(self, product_ids):
        products = self._queryset().filter(pk__in=product_ids)
        return [to_product(product) for product in products]

    def get_detail_by_slug(self, slug):
        product = self._queryset().filter(slug=slug).first()
        if product is None:
            return None, []
        related = self.list_active(category=product.category, exclude_slug=slug, limit=2)
        return to_product(product), related
