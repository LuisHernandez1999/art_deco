from django.contrib import admin

from shop.models import CarouselSlide, Order, OrderItem, Product


@admin.register(CarouselSlide)
class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ("title", "page", "order", "is_active")
    list_filter = ("page", "is_active")
    search_fields = ("title", "eyebrow", "copy")
    ordering = ("page", "order")
    fieldsets = (
        ("Exibição", {"fields": ("page", "order", "is_active", "eyebrow", "title", "accent", "copy")}),
        ("Imagem", {"fields": ("image_url", "image_alt")}),
        ("Ação", {"fields": ("button_label", "button_url")}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price_from", "featured", "is_active")
    list_filter = ("category", "featured", "is_active")
    search_fields = ("name", "summary", "description")
    prepopulated_fields = {"slug": ("name",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "quantity", "unit_price", "requires_quote")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("reference", "customer_name", "phone", "status", "payment_method", "total", "created_at")
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("customer_name", "phone", "reference")
    readonly_fields = ("reference", "created_at", "total")
    inlines = (OrderItemInline,)