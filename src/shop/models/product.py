from django.db import models


class Product(models.Model):
    class Category(models.TextChoices):
        MOLDURAS = "molduras", "Molduras"
        BOISERIE = "boiserie", "Boiserie"
        SANCAS = "sancas", "Sancas"
        PAINEIS = "paineis", "Painéis"
        JARDIM = "jardim", "Jardim"
        REPAROS = "reparos", "Reparos"
        FIBRA = "fibra", "Fibra de vidro"

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=24, choices=Category.choices)
    summary = models.CharField(max_length=220)
    description = models.TextField()
    price_from = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    image_url = models.CharField(max_length=320, blank=True)
    image_alt = models.CharField(max_length=180, blank=True)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-featured", "name"]
        indexes = [
            models.Index(fields=["is_active", "category", "featured"], name="shop_prod_catalog_idx"),
        ]

    def __str__(self):
        return self.name
