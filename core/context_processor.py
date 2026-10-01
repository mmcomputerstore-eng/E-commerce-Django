from core.models import (
    Category,
    Vendor,
    Products,
    ProductImage,
    CartOrders,
    CartOrdersItems,
    ProductReview,
    Wishlist,
    Address,
)


from taggit.models import Tag


def default(request):
    categories = Category.objects.all()
    all_tags = Tag.objects.all()

    cart_data = request.session.get('cart_data_obj', {})
    cart_count = sum(int(item.get('qty', 1)) for item in cart_data.values()) if cart_data else 0
    cart_total_amount = sum(float(item.get('price', 0)) * int(item.get('qty', 1)) for item in cart_data.values()) if cart_data else 0.0

    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return {
        'categories': categories,
        'all_tags': all_tags,
        'cart_data': cart_data,
        'cart_count': cart_count,
        'cart_total_amount': f"{cart_total_amount:.2f}",
        'cart_total_float': cart_total_amount,
        'wishlist_count': wishlist_count,
    }