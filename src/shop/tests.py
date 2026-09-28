from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from shop.models import CarouselSlide, Order, OrderItem, Product


class StorefrontFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(
            slug="moldura-teste",
            name="Moldura de teste",
            category=Product.Category.MOLDURAS,
            summary="Perfil de teste",
            description="Descrição de teste",
            price_from=Decimal("40.00"),
        )

    def test_home_and_catalog_render(self):
        self.assertEqual(self.client.get(reverse("shop:home")).status_code, 200)
        response = self.client.get(reverse("shop:catalog"), {"categoria": "molduras"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Moldura de teste")

    def test_home_and_about_only_show_active_slides_for_their_page(self):
        home_slide = CarouselSlide.objects.create(
            page=CarouselSlide.Page.HOME,
            title="Trabalho que permanece",
            image_url="/static/shop/img/artdecor-profile-work.jpg",
            image_alt="Acabamento de gesso",
        )
        CarouselSlide.objects.create(
            page=CarouselSlide.Page.HOME,
            title="Slide desativado",
            image_url="/static/shop/img/artdecor-interior.webp",
            image_alt="Molduras de gesso",
            is_active=False,
        )
        about_slide = CarouselSlide.objects.create(
            page=CarouselSlide.Page.ABOUT,
            title="Uma história feita à mão",
            image_url="/static/shop/img/artdecor-interior.webp",
            image_alt="Ateliê Art Decor",
        )

        home = self.client.get(reverse("shop:home"))
        about = self.client.get(reverse("shop:about"))

        self.assertEqual([slide.id for slide in home.context["carousel_slides"]], [home_slide.id])
        self.assertEqual([slide.id for slide in about.context["carousel_slides"]], [about_slide.id])
        self.assertNotContains(home, "Slide desativado")

    def test_catalog_paginates_and_preserves_category_and_search(self):
        Product.objects.bulk_create([
            Product(
                slug=f"moldura-extra-{index}",
                name=f"Moldura extra {index}",
                category=Product.Category.MOLDURAS,
                summary="Perfil de teste",
                description="Descrição de teste",
                price_from=Decimal("30.00"),
            )
            for index in range(7)
        ])

        first_page = self.client.get(reverse("shop:catalog"), {"categoria": "molduras", "q": "moldura"})
        second_page = self.client.get(
            reverse("shop:catalog"), {"categoria": "molduras", "q": "moldura", "page": "2"}
        )

        self.assertEqual(first_page.context["catalog_page"].count, 8)
        self.assertEqual(len(first_page.context["products"]), 6)
        self.assertContains(first_page, "categoria=molduras&amp;q=moldura&amp;page=2")
        self.assertEqual(second_page.context["catalog_page"].number, 2)
        self.assertEqual(len(second_page.context["products"]), 2)

    def test_order_flow_saves_order_and_clears_cart(self):
        self.client.post(reverse("shop:cart_add", kwargs={"slug": self.product.slug}))
        self.client.post(reverse("shop:cart_add", kwargs={"slug": self.product.slug}))

        response = self.client.post(reverse("shop:checkout"), {
            "customer_name": "Maria da Silva",
            "phone": "62999990000",
            "address": "Rua das Flores, 10",
            "city": "Goiânia",
            "notes": "Ligar à tarde",
            "payment_method": "pix",
        })

        order = Order.objects.get()
        self.assertRedirects(
            response,
            reverse("shop:order_confirmation", kwargs={"reference": order.reference}),
        )
        self.assertEqual(order.total, Decimal("80.00"))
        self.assertEqual(order.payment_method, Order.PaymentMethod.PIX)
        self.assertEqual(OrderItem.objects.get(order=order).quantity, 2)
        self.assertEqual(self.client.session.get("cart"), {})

    def test_checkout_rejects_invalid_payment_choice(self):
        self.client.post(reverse("shop:cart_add", kwargs={"slug": self.product.slug}))
        response = self.client.post(reverse("shop:checkout"), {
            "customer_name": "Maria",
            "phone": "62999990000",
            "payment_method": "card-number-4111",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Order.objects.exists())

    def test_order_confirmation_is_not_found_for_unknown_reference(self):
        response = self.client.get(reverse(
            "shop:order_confirmation",
            kwargs={"reference": "11111111-1111-4111-8111-111111111111"},
        ))
        self.assertEqual(response.status_code, 404)

    def test_add_to_cart_returns_fast_json_feedback(self):
        response = self.client.post(
            reverse("shop:cart_add", kwargs={"slug": self.product.slug}),
            HTTP_ACCEPT="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["cart_count"], 1)
        self.assertEqual(response.json()["quantity"], 1)