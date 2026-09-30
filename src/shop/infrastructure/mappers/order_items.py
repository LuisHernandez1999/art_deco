from shop.domain.entities.orders import OrderLine, OrderLineRequest
from shop.models import Order as OrderModel
from shop.models import OrderItem as OrderItemModel
from shop.models import Product as ProductModel


def to_order_line(product: ProductModel, request: OrderLineRequest) -> OrderLine:
    return OrderLine(
        product_id=product.pk,
        product_name=product.name,
        quantity=request.quantity,
        unit_price=product.price_from,
    )


def to_order_item_model(
    order: OrderModel,
    product: ProductModel,
    line: OrderLine,
) -> OrderItemModel:
    return OrderItemModel(
        order=order,
        product=product,
        product_name=line.product_name,
        quantity=line.quantity,
        unit_price=line.unit_price,
        requires_quote=line.requires_quote,
    )
