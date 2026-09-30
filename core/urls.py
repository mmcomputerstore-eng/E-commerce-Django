from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('',views.index,name='home'),
    path('products/',views.products_list_view,name='products'),
    path('products/tag/<slug:tag_slug>/', views.tag_list_view, name='tags'),
    path('product/<str:pid>/', views.product_details_view, name='product-details'),

    path('vendors/', views.vendor_list_view, name='vendors'),
    path('vendors/<str:vid>/', views.vendor_details_view, name='vendor_details'),
    # add reviews
    path('ajax-add-review/<str:pid>/', views.ajax_add_review, name='ajax_add_review'),
    # search
    path('search/', views.search_view, name='search'),

    # cart
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('delete-from-cart/', views.delete_from_cart, name='delete-from-cart'),
    path('update-cart/', views.update_cart, name='update-cart'),
    path('clear-cart/', views.clear_cart, name='clear-cart'),
]
