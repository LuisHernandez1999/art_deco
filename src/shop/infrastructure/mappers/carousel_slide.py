from shop.domain.entities.site_content import CarouselSlide


def to_carousel_slide(model) -> CarouselSlide:
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
