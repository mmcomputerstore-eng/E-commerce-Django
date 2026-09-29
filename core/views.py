from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q

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
    products = Products.objects.filter(featured=True, product_status='published')
    context = {
        'products': products
    }
    return render(request, 'core/index.html', context)


def products_list_view(request):
    category_param = request.GET.get('category')
    vendor_param = request.GET.get('vendor')

    base_products = Products.objects.filter(product_status='published')
    selected_category = None
    selected_vendor = None

    if category_param:
        if category_param.isdigit():
            selected_category = Category.objects.filter(id=category_param).first()
            base_products = base_products.filter(Q(category__id=category_param) | Q(category__cid=category_param))
        else:
            selected_category = Category.objects.filter(Q(cid=category_param) | Q(title__iexact=category_param)).first()
            base_products = base_products.filter(Q(category__cid=category_param) | Q(category__title__iexact=category_param))

    if vendor_param:
        if vendor_param.isdigit():
            selected_vendor = Vendor.objects.filter(id=vendor_param).first()
            base_products = base_products.filter(Q(vendor__id=vendor_param) | Q(vendor__vid=vendor_param))
        else:
            selected_vendor = Vendor.objects.filter(Q(vid=vendor_param) | Q(title__iexact=vendor_param)).first()
            base_products = base_products.filter(Q(vendor__vid=vendor_param) | Q(vendor__title__iexact=vendor_param))

    featured_products = base_products.filter(featured=True).order_by('-id')
    unfeatured_products = base_products.filter(featured=False).order_by('-id')
    products = base_products.order_by('-featured', '-id')

    categories = Category.objects.annotate(
        product_count=Count('category', filter=Q(category__product_status='published'))
    )
    vendors = Vendor.objects.annotate(
        product_count=Count('products', filter=Q(products__product_status='published'))
    )

    context = {
        'products': products,
        'featured_products': featured_products,
        'unfeatured_products': unfeatured_products,
        'categories': categories,
        'vendors': vendors,
        'selected_category': selected_category,
        'selected_vendor': selected_vendor,
        'category_param': category_param,
        'vendor_param': vendor_param,
    }
    return render(request, 'core/product_list.html', context)


def vendor_list_view(request):
    vendors = Vendor.objects.annotate(
        product_count=Count('products', filter=Q(products__product_status='published'))
    ).order_by('-date', '-id')
    context = {
        'vendors': vendors,
    }
    return render(request, 'core/vendor_list.html', context)


def vendor_details_view(request, vid):
    vendor = get_object_or_404(Vendor, vid=vid)
    products = Products.objects.filter(vendor=vendor, product_status='published').order_by('-featured', '-id')
    context = {
        'vendor': vendor,
        'products': products,
    }
    return render(request, 'core/vendor_details.html', context)


def product_details_view(request, pid):
    product = get_object_or_404(Products, pid=pid)
    p_images = ProductImage.objects.filter(product=product)

    if product.category:
        related_products = Products.objects.filter(
            category=product.category,
            product_status='published'
        ).exclude(pid=pid).order_by('-featured', '-id')[:4]
    else:
        related_products = Products.objects.filter(
            product_status='published'
        ).exclude(pid=pid).order_by('-featured', '-id')[:4]

    reviews = ProductReview.objects.filter(product=product).order_by('-date')

    context = {
        'product': product,
        'p_images': p_images,
        'related_products': related_products,
        'reviews': reviews,
    }
    return render(request, 'core/product_details.html', context)

