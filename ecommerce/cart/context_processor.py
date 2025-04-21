def cart_total(request):
    total_items = 0
    cart = request.session.get('cart', {})

    for item in cart.values():
        total_items += item['quantity']

    return {'total_cart_items': total_items}