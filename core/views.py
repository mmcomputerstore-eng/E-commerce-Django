from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q, Avg, Min, Max
from taggit.models import Tag
from core.forms import ProductReviewForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

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


def index(request):
    products = Products.objects.filter(
        featured=True, product_status='published'
    ).annotate(
        avg_rating=Avg('productreview__rating'),
        review_count=Count('productreview')
    ).prefetch_related('tags')

    banner_product_1 = Products.objects.filter(title='MacBook Air Latest Model', product_status='published').first()
    banner_product_2 = Products.objects.filter(title='Original Outdoor Beanbag', product_status='published').first()
    banner_product_3 = Products.objects.filter(title='Tan Suede Biker Jacket', product_status='published').first()

    context = {
        'products': products,
        'banner_product_1': banner_product_1,
        'banner_product_2': banner_product_2,
        'banner_product_3': banner_product_3,
    }
    return render(request, 'core/index.html', context)



def products_list_view(request, tag_slug=None):
    category_param = request.GET.get('category')
    vendor_param = request.GET.get('vendor')
    tag_param = tag_slug or request.GET.get('tag')
    q_param = request.GET.get('q')

    base_products = Products.objects.filter(product_status='published').annotate(
        avg_rating=Avg('productreview__rating'),
        review_count=Count('productreview')
    )
    selected_category = None
    selected_vendor = None
    selected_tag = None

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

    if tag_param:
        selected_tag = Tag.objects.filter(Q(slug=tag_param) | Q(name__iexact=tag_param)).first()
        if selected_tag:
            base_products = base_products.filter(tags__in=[selected_tag])
        else:
            base_products = base_products.filter(tags__name__iexact=tag_param)

    if q_param:
        base_products = base_products.filter(
            Q(title__icontains=q_param) |
            Q(description__icontains=q_param) |
            Q(tags__name__icontains=q_param)
        )

    # Price Filtering
    min_price_param = request.GET.get('min_price')
    max_price_param = request.GET.get('max_price')

    if min_price_param:
        try:
            base_products = base_products.filter(price__gte=float(min_price_param))
        except (ValueError, TypeError):
            min_price_param = None

    if max_price_param:
        try:
            base_products = base_products.filter(price__lte=float(max_price_param))
        except (ValueError, TypeError):
            max_price_param = None

    base_products = base_products.distinct().prefetch_related('tags')

    featured_products = base_products.filter(featured=True).order_by('-id')
    unfeatured_products = base_products.filter(featured=False).order_by('-id')
    products = base_products.order_by('-featured', '-id')

    # Get min & max price from database for slider bounds
    price_stats = Products.objects.filter(product_status='published').aggregate(
        min_p=Min('price'),
        max_p=Max('price')
    )
    db_min_price = int(price_stats['min_p']) if price_stats['min_p'] is not None else 0
    db_max_price = int(price_stats['max_p']) + 50 if price_stats['max_p'] is not None else 1000

    categories = Category.objects.annotate(
        product_count=Count('category', filter=Q(category__product_status='published'))
    )
    vendors = Vendor.objects.annotate(
        product_count=Count('products', filter=Q(products__product_status='published'))
    )
    tags = Tag.objects.annotate(
        product_count=Count('products', filter=Q(products__product_status='published'))
    ).filter(product_count__gt=0).order_by('-product_count', 'name')

    context = {
        'products': products,
        'featured_products': featured_products,
        'unfeatured_products': unfeatured_products,
        'categories': categories,
        'vendors': vendors,
        'tags': tags,
        'selected_category': selected_category,
        'selected_vendor': selected_vendor,
        'selected_tag': selected_tag,
        'category_param': category_param,
        'vendor_param': vendor_param,
        'tag_param': tag_param,
        'q_param': q_param,
        'min_price_param': min_price_param,
        'max_price_param': max_price_param,
        'db_min_price': db_min_price,
        'db_max_price': db_max_price,
    }
    return render(request, 'core/product_list.html', context)


def tag_list_view(request, tag_slug):
    return products_list_view(request, tag_slug=tag_slug)


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
    products = Products.objects.filter(
        vendor=vendor, product_status='published'
    ).annotate(
        avg_rating=Avg('productreview__rating'),
        review_count=Count('productreview')
    ).prefetch_related('tags').order_by('-featured', '-id')
    context = {
        'vendor': vendor,
        'products': products,
    }
    return render(request, 'core/vendor_details.html', context)


def product_details_view(request, pid):
    product = get_object_or_404(Products.objects.prefetch_related('tags'), pid=pid)
    p_images = ProductImage.objects.filter(product=product)

    # Use taggit's similar_objects to find related products by matching tags, fallback to category
    related_products = product.tags.similar_objects()[:4]
    if not related_products:
        if product.category:
            related_products = Products.objects.filter(
                category=product.category,
                product_status='published'
            ).exclude(pid=pid).order_by('-featured', '-id')[:4]
        else:
            related_products = Products.objects.filter(
                product_status='published'
            ).exclude(pid=pid).order_by('-featured', '-id')[:4]

    review_form = ProductReviewForm()
    reviews = ProductReview.objects.filter(product=product).order_by('-date')
    rating_agg = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    avrage_rating = ((rating_agg['rating'] or 0) / 5) * 100
    context = {
        'product': product,
        'review_form': review_form,
        'p_images': p_images,
        'related_products': related_products,
        'reviews': reviews,
        'avrage_rating': avrage_rating,
    }
    return render(request, 'core/product_details.html', context)


def ajax_add_review(request, pid):
    product = get_object_or_404(Products, pid=pid)
    user = request.user if request.user.is_authenticated else None

    review_text = request.POST.get('review', '').strip()
    rating_val = request.POST.get('rating', '5')

    if not review_text:
        return JsonResponse({'bool': False, 'error': 'Review cannot be empty.'}, status=400)

    try:
        rating_int = int(rating_val)
    except (ValueError, TypeError):
        rating_int = 5

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=review_text,
        rating=rating_int
    )

    avg_data = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    avg_rating = avg_data['rating'] or 0
    rating_percent = round((avg_rating / 5) * 100, 1)
    reviews_count = ProductReview.objects.filter(product=product).count()

    context = {
        'user': user.username.title() if user else 'Anonymous Guest',
        'review': review.review,
        'rating': review.rating,
        'date': review.date.strftime("%B %d, %Y"),
    }

    return JsonResponse({
        'bool': True,
        'context': context,
        'average_reviews': avg_data,
        'rating_percent': rating_percent,
        'reviews_count': reviews_count,
        'avg_rating': round(avg_rating, 1),
    })


def search_view(request):
    query = request.GET.get('q', '').strip()
    category_param = request.GET.get('category')
    min_price_param = request.GET.get('min_price')
    max_price_param = request.GET.get('max_price')

    if query:
        products = Products.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query),
            product_status='published'
        )
    else:
        products = Products.objects.filter(product_status='published')

    if category_param:
        products = products.filter(Q(category__cid=category_param) | Q(category__id=category_param))

    if min_price_param:
        try:
            products = products.filter(price__gte=float(min_price_param))
        except (ValueError, TypeError):
            min_price_param = None

    if max_price_param:
        try:
            products = products.filter(price__lte=float(max_price_param))
        except (ValueError, TypeError):
            max_price_param = None

    products = products.distinct().annotate(
        avg_rating=Avg('productreview__rating'),
        review_count=Count('productreview')
    ).prefetch_related('tags').order_by('-featured', '-id')

    price_stats = Products.objects.filter(product_status='published').aggregate(
        min_p=Min('price'),
        max_p=Max('price')
    )
    db_min_price = int(price_stats['min_p']) if price_stats['min_p'] is not None else 0
    db_max_price = int(price_stats['max_p']) + 50 if price_stats['max_p'] is not None else 1000

    context = {
        'products': products,
        'query': query,
        'category_param': category_param,
        'min_price_param': min_price_param,
        'max_price_param': max_price_param,
        'db_min_price': db_min_price,
        'db_max_price': db_max_price,
    }

    return render(request, 'core/search.html', context)


def cart_view(request):
    cart_data = request.session.get('cart_data_obj', {})
    cart_count = sum(int(item.get('qty', 1)) for item in cart_data.values()) if cart_data else 0
    cart_total_amount = sum(float(item.get('price', 0)) * int(item.get('qty', 1)) for item in cart_data.values()) if cart_data else 0.0
    context = {
        'cart_data': cart_data,
        'cart_count': cart_count,
        'cart_total_amount': f"{cart_total_amount:.2f}",
    }
    return render(request, 'core/cart.html', context)


def add_to_cart(request):
    p_id = str(request.POST.get('id') or request.GET.get('id') or request.POST.get('pid') or request.GET.get('pid') or '').strip()
    try:
        qty = int(request.POST.get('qty') or request.GET.get('qty') or 1)
        if qty < 1:
            qty = 1
    except (ValueError, TypeError):
        qty = 1

    if not p_id:
        return JsonResponse({'status': 'error', 'message': 'Product ID is missing.'}, status=400)

    product = Products.objects.filter(pid=p_id).first()
    if not product and p_id.isdigit():
        product = Products.objects.filter(id=int(p_id)).first()

    if not product:
        return JsonResponse({'status': 'error', 'message': 'Product not found.'}, status=404)

    cart_data = request.session.get('cart_data_obj', {})
    pid_key = str(product.pid)

    if pid_key in cart_data:
        cart_data[pid_key]['qty'] = int(cart_data[pid_key]['qty']) + qty
        cart_data[pid_key]['total_price'] = round(float(cart_data[pid_key]['price']) * cart_data[pid_key]['qty'], 2)
    else:
        image_url = product.image.url if product.image else ''
        cart_data[pid_key] = {
            'pid': product.pid,
            'id': product.id,
            'title': product.title,
            'qty': qty,
            'price': str(product.price),
            'image': image_url,
            'total_price': round(float(product.price) * qty, 2),
        }

    request.session['cart_data_obj'] = cart_data
    request.session.modified = True

    cart_count = sum(int(item['qty']) for item in cart_data.values())
    cart_total = sum(float(item['price']) * int(item['qty']) for item in cart_data.values())

    return JsonResponse({
        'status': 'success',
        'message': f"Added '{product.title}' to cart!",
        'cart_count': cart_count,
        'cart_total': f"{cart_total:.2f}",
        'item': cart_data[pid_key],
        'cart_data': cart_data,
    })


def delete_from_cart(request):
    p_id = str(request.POST.get('id') or request.GET.get('id') or request.POST.get('pid') or request.GET.get('pid') or '').strip()
    cart_data = request.session.get('cart_data_obj', {})

    matched_key = None
    if p_id in cart_data:
        matched_key = p_id
    else:
        for k, v in cart_data.items():
            if str(v.get('id')) == p_id or str(v.get('pid')) == p_id:
                matched_key = k
                break

    if matched_key and matched_key in cart_data:
        del cart_data[matched_key]
        request.session['cart_data_obj'] = cart_data
        request.session.modified = True

    cart_count = sum(int(item['qty']) for item in cart_data.values()) if cart_data else 0
    cart_total = sum(float(item['price']) * int(item['qty']) for item in cart_data.values()) if cart_data else 0.0

    return JsonResponse({
        'status': 'success',
        'cart_count': cart_count,
        'cart_total': f"{cart_total:.2f}",
        'cart_data': cart_data,
    })


def update_cart(request):
    p_id = str(request.POST.get('id') or request.GET.get('id') or request.POST.get('pid') or request.GET.get('pid') or '').strip()
    try:
        qty = int(request.POST.get('qty') or request.GET.get('qty') or 1)
    except (ValueError, TypeError):
        qty = 1

    cart_data = request.session.get('cart_data_obj', {})
    matched_key = None
    if p_id in cart_data:
        matched_key = p_id
    else:
        for k, v in cart_data.items():
            if str(v.get('id')) == p_id or str(v.get('pid')) == p_id:
                matched_key = k
                break

    item_total = 0.0
    if matched_key and matched_key in cart_data:
        if qty <= 0:
            del cart_data[matched_key]
        else:
            cart_data[matched_key]['qty'] = qty
            cart_data[matched_key]['total_price'] = round(float(cart_data[matched_key]['price']) * qty, 2)
            item_total = cart_data[matched_key]['total_price']

        request.session['cart_data_obj'] = cart_data
        request.session.modified = True

    cart_count = sum(int(item['qty']) for item in cart_data.values()) if cart_data else 0
    cart_total = sum(float(item['price']) * int(item['qty']) for item in cart_data.values()) if cart_data else 0.0

    return JsonResponse({
        'status': 'success',
        'cart_count': cart_count,
        'cart_total': f"{cart_total:.2f}",
        'item_total': f"{item_total:.2f}",
        'cart_data': cart_data,
    })


def clear_cart(request):
    if 'cart_data_obj' in request.session:
        del request.session['cart_data_obj']
        request.session.modified = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax'):
        return JsonResponse({'status': 'success', 'cart_count': 0, 'cart_total': '0.00'})

    return redirect('core:cart')


@login_required
def checkout_view(request):
    cart_data = request.session.get('cart_data_obj', {})
    if not cart_data:
        messages.warning(request, "Your cart is empty. Please add items before checking out.")
        return redirect('core:cart')

    cart_count = sum(int(item.get('qty', 1)) for item in cart_data.values())
    cart_total_amount = sum(float(item.get('price', 0)) * int(item.get('qty', 1)) for item in cart_data.values())

    addresses = Address.objects.filter(user=request.user).order_by('-status', '-id')
    active_address = Address.objects.filter(user=request.user, status=True).first()

    # If user has addresses but none marked active, activate the first one
    if not active_address and addresses.exists():
        active_address = addresses.first()
        active_address.status = True
        active_address.save()

    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address_id')
        new_address_text = request.POST.get('new_address', '').strip()

        # Handle newly entered address during checkout
        if new_address_text:
            Address.objects.filter(user=request.user).update(status=False)
            active_address = Address.objects.create(
                user=request.user,
                address=new_address_text,
                status=True
            )
        elif selected_address_id:
            chosen_addr = Address.objects.filter(id=selected_address_id, user=request.user).first()
            if chosen_addr:
                Address.objects.filter(user=request.user).update(status=False)
                chosen_addr.status = True
                chosen_addr.save()
                active_address = chosen_addr

        # Validate that an active address exists
        if not active_address:
            messages.error(request, "Please enter or select an active shipping address to place your order.")
            return redirect('core:checkout')

        # Create CartOrders record
        order = CartOrders.objects.create(
            user=request.user,
            price=round(cart_total_amount, 2),
            paid_status=False,
            product_status='processing'
        )

        # Create CartOrdersItems records
        for pid, item in cart_data.items():
            CartOrdersItems.objects.create(
                order=order,
                product_status='processing',
                items=item['title'],
                quantity=int(item['qty']),
                price=float(item['price']),
                total=float(item['total_price']),
            )

        # Clear cart session
        if 'cart_data_obj' in request.session:
            del request.session['cart_data_obj']
            request.session.modified = True

        messages.success(request, f"Order #{order.id} has been placed successfully!")
        return redirect('core:order-completed', oid=order.id)

    context = {
        'cart_data': cart_data,
        'cart_count': cart_count,
        'cart_total_amount': f"{cart_total_amount:.2f}",
        'addresses': addresses,
        'active_address': active_address,
    }
    return render(request, 'core/checkout.html', context)


@login_required
def make_address_default(request):
    addr_id = request.POST.get('id') or request.GET.get('id')
    if not addr_id:
        return JsonResponse({'status': 'error', 'message': 'Address ID missing.'}, status=400)

    addr = Address.objects.filter(id=addr_id, user=request.user).first()
    if not addr:
        return JsonResponse({'status': 'error', 'message': 'Address not found.'}, status=404)

    Address.objects.filter(user=request.user).update(status=False)
    addr.status = True
    addr.save()

    return JsonResponse({
        'status': 'success',
        'message': 'Active shipping address updated!',
        'address_id': addr.id,
        'address_text': addr.address,
    })


@login_required
def save_address(request):
    address_text = request.POST.get('address', '').strip()
    if not address_text:
        return JsonResponse({'status': 'error', 'message': 'Address cannot be empty.'}, status=400)

    Address.objects.filter(user=request.user).update(status=False)
    new_addr = Address.objects.create(
        user=request.user,
        address=address_text,
        status=True
    )

    return JsonResponse({
        'status': 'success',
        'message': 'New address saved and set as active!',
        'address_id': new_addr.id,
        'address_text': new_addr.address,
    })


@login_required
def order_completed_view(request, oid):
    order = get_object_or_404(CartOrders, id=oid, user=request.user)
    order_items = CartOrdersItems.objects.filter(order=order)
    active_address = Address.objects.filter(user=request.user, status=True).first()

    context = {
        'order': order,
        'order_items': order_items,
        'active_address': active_address,
    }
    return render(request, 'core/order_completed.html', context)


@login_required
def customer_dashboard(request):
    orders = CartOrders.objects.filter(user=request.user).order_by('-order_date', '-id').prefetch_related('cartordersitems_set')
    orders_processing = [o for o in orders if o.product_status == 'processing']
    orders_shipped = [o for o in orders if o.product_status == 'shipped']
    orders_delivered = [o for o in orders if o.product_status == 'delivered']

    total_orders_count = len(orders)
    processing_count = len(orders_processing)
    shipped_count = len(orders_shipped)
    delivered_count = len(orders_delivered)
    total_spent = sum(float(o.price) for o in orders)

    addresses = Address.objects.filter(user=request.user).order_by('-status', '-id')
    active_address = Address.objects.filter(user=request.user, status=True).first()

    if not active_address and addresses.exists():
        active_address = addresses.first()
        active_address.status = True
        active_address.save()

    # Handle profile details update
    if request.method == 'POST' and 'update_profile' in request.POST:
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        bio = request.POST.get('bio', '').strip()

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.bio = bio
        request.user.save()
        messages.success(request, 'Your profile details have been updated successfully.')
        return redirect('core:customer-dashboard')

    # Handle password change
    if request.method == 'POST' and 'change_password' in request.POST:
        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password entered is incorrect.')
        elif len(new_password) < 6:
            messages.error(request, 'New password must be at least 6 characters long.')
        elif new_password != confirm_password:
            messages.error(request, 'New password and confirmation password do not match.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Your password was updated successfully!')
        return redirect('core:customer-dashboard')

    context = {
        'orders': orders,
        'orders_processing': orders_processing,
        'orders_shipped': orders_shipped,
        'orders_delivered': orders_delivered,
        'total_orders_count': total_orders_count,
        'processing_count': processing_count,
        'shipped_count': shipped_count,
        'delivered_count': delivered_count,
        'total_spent': f"{total_spent:.2f}",
        'addresses': addresses,
        'active_address': active_address,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def delete_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('id')
        address = Address.objects.filter(id=address_id, user=request.user).first()
        if address:
            was_active = address.status
            address.delete()

            next_active_text = ''
            next_active_id = None
            if was_active:
                next_address = Address.objects.filter(user=request.user).first()
                if next_address:
                    next_address.status = True
                    next_address.save()
                    next_active_text = next_address.address
                    next_active_id = next_address.id

            return JsonResponse({
                'status': 'success',
                'message': 'Address removed successfully.',
                'was_active': was_active,
                'next_active_id': next_active_id,
                'next_active_text': next_active_text,
                'remaining_count': Address.objects.filter(user=request.user).count()
            })
        return JsonResponse({'status': 'error', 'message': 'Address not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


@login_required
def order_detail_view(request, oid):
    order = get_object_or_404(CartOrders, id=oid, user=request.user)
    order_items = CartOrdersItems.objects.filter(order=order)
    active_address = Address.objects.filter(user=request.user, status=True).first()

    context = {
        'order': order,
        'order_items': order_items,
        'active_address': active_address,
    }
    return render(request, 'core/order_detail.html', context)


@login_required
def order_detail_ajax(request, oid):
    order = get_object_or_404(CartOrders, id=oid, user=request.user)
    order_items = CartOrdersItems.objects.filter(order=order)
    active_address = Address.objects.filter(user=request.user, status=True).first()

    items_list = []
    for item in order_items:
        items_list.append({
            'title': item.items,
            'qty': item.quantity,
            'price': str(item.price),
            'total': str(item.total),
        })

    return JsonResponse({
        'status': 'success',
        'order': {
            'id': order.id,
            'date': order.order_date.strftime('%B %d, %Y - %I:%M %p'),
            'price': str(order.price),
            'status': order.product_status,
            'paid_status': order.paid_status,
            'address': active_address.address if active_address else 'Not specified',
            'items': items_list,
        }
    })


