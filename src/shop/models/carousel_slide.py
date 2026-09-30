from django.db import models


class CarouselSlide(models.Model):
    class Page(models.TextChoices):
        HOME = "home", "Página inicial"
        ABOUT = "about", "Sobre"

    page = models.CharField(max_length=12, choices=Page.choices, db_index=True)
    eyebrow = models.CharField(max_length=80, blank=True)
    title = models.CharField(max_length=150)
    accent = models.CharField(max_length=100, blank=True)
    copy = models.CharField(max_length=260, blank=True)
    image_url = models.CharField(max_length=320)
    image_alt = models.CharField(max_length=180)
    button_label = models.CharField(max_length=60, blank=True)
    button_url = models.CharField(max_length=320, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "pk"]
        indexes = [models.Index(fields=["page", "is_active", "order"], name="shop_slide_live_order_idx")]

    def __str__(self):
        return f"{self.get_page_display()} · {self.title}"
