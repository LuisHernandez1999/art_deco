from uuid import UUID

from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render

from shop.application.use_cases import BuildCart, PlaceOrder
from shop.infrastructure.repositories.catalog import DjangoCatalogRepository
from shop.infrastructure.repositories.orders import DjangoOrderRepository
from shop.infrastructure.repositories.site_content import DjangoSiteContentRepository


catalog_repository = DjangoCatalogRepository()
site_content_repository = DjangoSiteContentRepository()
order_repository = DjangoOrderRepository()


def home(request):
    featured = catalog_repository.list_active(limit=4)
    return render(request, "shop/home.html", {
        "featured_products": featured,
        "carousel_slides": site_content_repository.list_carousel("home"),
    })


def about(request):
    return render(request, "shop/about.html", {
        "about_carousel_slides": site_content_repository.list_carousel("about"),
        "about_second_carousel_slides": site_content_repository.list_carousel("about_2"),
    })


def information(request):
    return render(request, "shop/information.html")


def catalog(request):
    selected_category = request.GET.get("categoria", "")
    query = request.GET.get("q", "").strip()
    page = catalog_repository.list_active_page(
        category=selected_category,
        query=query,
        page_number=request.GET.get("page", 1),
    )
    page_links = []
    for page_number in range(max(1, page.number - 2), min(page.num_pages, page.number + 2) + 1):
        query_params = request.GET.copy()
        query_params["page"] = page_number
        page_links.append({"number": page_number, "url": f"?{query_params.urlencode()}", "current": page_number == page.number})
    categories = catalog_repository.list_categories()
    return render(request, "shop/catalog.html", {
        "products": page.items,
        "catalog_page": page,
        "page_links": page_links,
        "categories": categories,
        "selected_category": selected_category,
        "query": query,
    })


def product_detail(request, slug):
    product, related = catalog_repository.get_detail_by_slug(slug)
    if product is None:
        raise Http404
    return render(request, "shop/product_detail.html", {
        "product": product,
        "related_products": related,
    })


def cart_contents(request):
    summary = BuildCart(catalog_repository).execute(request.session.get("cart", {}))
    return {
        "lines": summary.lines,
        "total": summary.total,
        "quote_needed": summary.quote_needed,
    }


def cart(request):
    return render(request, "shop/cart.html", cart_contents(request))


def cart_add(request, slug):
    if request.method != "POST":
        raise Http404
    product = catalog_repository.get_by_slug(slug)
    if product is None:
        raise Http404
    cart = request.session.get("cart", {})
    product_id = str(product.id)
    cart[product_id] = min(int(cart.get(product_id, 0)) + 1, 20)
    request.session["cart"] = cart
    message = f"{product.name} foi adicionado ao seu pedido."
    if request.headers.get("Accept") == "application/json":
        return JsonResponse({
            "ok": True,
            "quantity": cart[product_id],
            "cart_count": sum(int(quantity) for quantity in cart.values()),
            "message": message,
        })
    messages.success(request, message)
    return redirect("shop:cart")


def cart_update(request, product_id):
    if request.method != "POST":
        raise Http404
    cart = request.session.get("cart", {})
    key = str(product_id)
    action = request.POST.get("action")
    if action == "remove" or key not in cart:
        cart.pop(key, None)
    else:
        try:
            quantity = int(request.POST.get("quantity", "1"))
        except ValueError:
            quantity = 1
        if quantity < 1:
            cart.pop(key, None)
        else:
            cart[key] = min(quantity, 20)
    request.session["cart"] = cart
    return redirect("shop:cart")


def checkout(request):
    details = cart_contents(request)
    if not details["lines"]:
        messages.info(request, "Seu carrinho está vazio. Escolha uma peça para continuar.")
        return redirect("shop:catalog")

    if request.method == "POST":
        try:
            receipt = PlaceOrder(order_repository).execute(
                customer_name=request.POST.get("customer_name", ""),
                phone=request.POST.get("phone", ""),
                address=request.POST.get("address", ""),
                city=request.POST.get("city", ""),
                notes=request.POST.get("notes", ""),
                payment_method=request.POST.get("payment_method", ""),
                cart=request.session.get("cart", {}),
            )
        except ValueError as error:
            messages.error(request, str(error))
            return render(request, "shop/checkout.html", {**details, "form_data": request.POST})
        request.session["cart"] = {}
        return redirect("shop:order_confirmation", reference=receipt.reference)

    return render(request, "shop/checkout.html", details)


def order_confirmation(request, reference):
    try:
        reference = UUID(str(reference))
    except ValueError as error:
        raise Http404 from error
    order = order_repository.get_order(reference)
    if order is None:
        raise Http404
    return render(request, "shop/order_confirmation.html", {"order": order})
