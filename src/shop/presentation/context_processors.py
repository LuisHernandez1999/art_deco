def site_context(request):
    cart = request.session.get("cart", {})
    return {
        "cart_count": sum(int(quantity) for quantity in cart.values()),
        "whatsapp_number": "5562982230022",
        "whatsapp_display": "(62) 9 8223-0022",
        "instagram_url": "https://www.instagram.com/gesso.artdecor/",
    }