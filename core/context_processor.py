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

    return {
        'categories': categories,
        'all_tags': all_tags,
    }