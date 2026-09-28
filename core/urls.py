from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('',views.index,name='home'),
    path('products/',views.products_list_view,name='products'),
]
