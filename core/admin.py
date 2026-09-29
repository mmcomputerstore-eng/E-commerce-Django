from django.contrib import admin
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


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductsAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = [
        'user',
        'title',
        'product_image',
        'price',
        'category',
        'display_tags',
        'featured',
        'product_status',
        'pid',
    ]
    list_editable = ['price', 'product_status', 'featured']
    list_filter = ['category', 'product_status', 'featured', 'in_stock']
    search_fields = ['title', 'description', 'pid', 'sku', 'tags__name']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def display_tags(self, obj):
        tags = [t.name for t in obj.tags.all()]
        return ", ".join(tags) if tags else "—"
    display_tags.short_description = 'Tags'



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image', 'cid']
    search_fields = ['title', 'cid']


class VendorAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'vendor_image',
        'vendor_cover_image',
        'user',
        'contact',
        'chat_resp_time',
        'ship_on_time',
        'days_return',
    ]
    search_fields = ['title', 'contact', 'address', 'user__username']


class CartOrdersItemsInline(admin.TabularInline):
    model = CartOrdersItems
    extra = 0


class CartOrdersAdmin(admin.ModelAdmin):
    inlines = [CartOrdersItemsInline]
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']
    list_editable = ['paid_status', 'product_status']
    list_filter = ['paid_status', 'product_status', 'order_date']
    search_fields = ['user__username', 'user__email']


class CartOrdersItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'items', 'product_status', 'quantity', 'price', 'total']
    search_fields = ['items', 'order__id', 'order__user__username']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'review', 'date']
    list_filter = ['rating', 'date']
    search_fields = ['user__username', 'product__title', 'review']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']
    search_fields = ['user__username', 'product__title']


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']
    list_editable = ['status']
    search_fields = ['user__username', 'address']


admin.site.register(Products, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrders, CartOrdersAdmin)
admin.site.register(CartOrdersItems, CartOrdersItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)