import uuid

from django.db import models


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
    product = models.ForeignKey("shop.Product", on_delete=models.PROTECT)
    product_name = models.CharField(max_length=120)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    requires_quote = models.BooleanField(default=False)

    def line_total(self):
        if self.requires_quote or self.unit_price is None:
            return None
        return self.unit_price * self.quantity
