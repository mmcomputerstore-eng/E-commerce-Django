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


def default(request):
    categories = Category.objects.all()

    return {
        'categories':categories,
    }