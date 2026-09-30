from shop.domain.entities.catalog import Product


def to_product(model) -> Product:
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
