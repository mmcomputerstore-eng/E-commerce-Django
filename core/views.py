from django.shortcuts import render

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


# Create your views here.
def index(request):
    products = Products.objects.all()
    context = {
        'products':products
    }
    return render(request,'core/index.html',context)

