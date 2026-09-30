from shop.infrastructure.mappers.carousel_slide import to_carousel_slide
from shop.models import CarouselSlide as CarouselSlideModel


class DjangoSiteContentRepository:
    def list_carousel(self, page):
        slides = CarouselSlideModel.objects.filter(page=page, is_active=True).only(
            "id", "page", "eyebrow", "title", "accent", "copy", "image_url",
            "image_alt", "button_label", "button_url",
        )
        return [to_carousel_slide(slide) for slide in slides]
