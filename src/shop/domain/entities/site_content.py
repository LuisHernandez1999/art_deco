from dataclasses import dataclass


@dataclass(frozen=True)
class CarouselSlide:
    id: int
    page: str
    eyebrow: str
    title: str
    accent: str
    copy: str
    image_url: str
    image_alt: str
    button_label: str
    button_url: str
