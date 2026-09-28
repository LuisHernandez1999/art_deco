from decimal import Decimal

from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q

from shop.domain.entities import CarouselSlide, CatalogPage, OrderReceipt, Product
from shop.models import CarouselSlide as CarouselSlideModel
from shop.models import Order, OrderItem, Product as ProductModel


def to_product(model):
    return Product(
        id=model.pk,
        slug=model.slug,
        name=model.name,
        category=model.get_category_display(),
        summary=model.summary,
        description=model.description,
        price_from=model.price_from,
        image_url=model.image_url,
        image_alt=model.image_alt,
        featured=model.featured,
    )


def to_carousel_slide(model):
    return CarouselSlide(
        id=model.pk,
        page=model.page,
        eyebrow=model.eyebrow,
        title=model.title,
        accent=model.accent,
        copy=model.copy,
        image_url=model.image_url,
        image_alt=model.image_alt,
        button_label=model.button_label,
        button_url=model.button_url,
    )


class DjangoSiteContentRepository:
    def list_carousel(self, page):
        slides = CarouselSlideModel.objects.filter(page=page, is_active=True).only(
            "id", "page", "eyebrow", "title", "accent", "copy", "image_url",
            "image_alt", "button_label", "button_url",
        )
        return [to_carousel_slide(slide) for slide in slides]


class DjangoCatalogRepository:
    def _queryset(self, category="", query="", exclude_slug=""):
        products = ProductModel.objects.filter(is_active=True)
        if category:
            products = products.filter(category=category)
        if query:
            products = products.filter(
                Q(name__icontains=query) | Q(summary__icontains=query)
            )
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

    def get_by_slug(self, slug):
        product = self._queryset().filter(slug=slug).first()
        return to_product(product) if product else None

    def get_detail_by_slug(self, slug):
        product = self._queryset().filter(slug=slug).first()
        if product is None:
            return None, []
        related = self.list_active(
            category=product.category,
            exclude_slug=slug,
            limit=2,
        )
        return to_product(product), related

    def get_by_id(self, product_id):
        product = self._queryset().filter(pk=product_id).first()
        return to_product(product) if product else None


class DjangoOrderRepository:
    @transaction.atomic
    def place_order(self, *, customer_name, phone, address, city, notes, payment_method, lines):
        product_ids = {line.product_id for line in lines}
        products = {
            product.pk: product
            for product in ProductModel.objects.filter(is_active=True, pk__in=product_ids)
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
        return Order.objects.prefetch_related("items").filter(reference=reference).first()