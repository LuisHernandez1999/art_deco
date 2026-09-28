import uuid

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


class Order(models.Model):
    class PaymentMethod(models.TextChoices):
        PIX = "pix", "Pix"
        CARD = "card", "Cartão na entrega/retirada"
        CASH = "cash", "Dinheiro"

    class Status(models.TextChoices):
        RECEIVED = "received", "Pedido recebido"
        CONTACTED = "contacted", "Em contato"
        APPROVED = "approved", "Aprovado"
        COMPLETED = "completed", "Concluído"

    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=24)
    address = models.CharField(max_length=220, blank=True)
    city = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    payment_method = models.CharField(max_length=12, choices=PaymentMethod.choices)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.RECEIVED)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Pedido {str(self.reference)[:8]} — {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=120)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    requires_quote = models.BooleanField(default=False)

    def line_total(self):
        if self.requires_quote or self.unit_price is None:
            return None
        return self.unit_price * self.quantity