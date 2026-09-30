from decimal import Decimal

from shop.domain.entities.cart import CartLine, CartSummary
from shop.domain.repositories.catalog import CatalogRepository


class BuildCart:
    """Build a priced snapshot of the product IDs and quantities in a session cart."""

    def __init__(self, catalog: CatalogRepository):
        self.catalog = catalog

    def execute(self, cart: dict[str, int]) -> CartSummary:
        products_by_id = {
            str(product.id): product
            for product in self.catalog.get_by_ids(cart.keys())
        }
        lines = []
        total = Decimal("0.00")
        quote_needed = False

        for product_id, quantity in cart.items():
            product = products_by_id.get(str(product_id))
            if product is None:
                continue
            quantity = int(quantity)
            line_total = product.price_from * quantity if product.price_from is not None else None
            if line_total is None:
                quote_needed = True
            else:
                total += line_total
            lines.append(CartLine(product=product, quantity=quantity, line_total=line_total))

        return CartSummary(lines=tuple(lines), total=total, quote_needed=quote_needed)
