/**
 * Shopping Cart Handler - Universal Add to Cart, Live Header Cart Sync, and Notifications
 */

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showCartToast(message, type) {
    type = type || 'success';
    let container = document.getElementById('cart-toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'cart-toast-container';
        container.style.cssText = 'position: fixed; bottom: 30px; right: 30px; z-index: 999999; display: flex; flex-direction: column; gap: 12px; max-width: 380px; pointer-events: none;';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'cart-toast-alert';
    const borderColor = type === 'success' ? '#28a745' : '#dc3545';
    const iconHtml = type === 'success' 
        ? '<span style="display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:#28a745; color:#fff; font-size:14px; margin-right:12px; flex-shrink:0;">✓</span>' 
        : '<span style="display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:#dc3545; color:#fff; font-size:14px; margin-right:12px; flex-shrink:0;">✕</span>';

    toast.style.cssText = `
        background-color: #222222;
        color: #ffffff;
        padding: 14px 20px;
        border-radius: 8px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        font-size: 1.35rem;
        font-weight: 500;
        border-left: 4px solid ${borderColor};
        pointer-events: auto;
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    `;
    toast.innerHTML = `
        <div style="display: flex; align-items: center; width: 100%;">
            ${iconHtml}
            <span style="flex-grow: 1; line-height: 1.4;">${message}</span>
        </div>
    `;

    container.appendChild(toast);

    requestAnimationFrame(function() {
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
    });

    setTimeout(function() {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px)';
        setTimeout(function() {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 3200);
}

function updateHeaderCartUI(data) {
    if (!data) return;

    // Update badge count
    const countEl = document.getElementById('headerCartCount');
    if (countEl) {
        countEl.textContent = data.cart_count;
    }

    // Update total price
    const totalEl = document.getElementById('headerCartTotal');
    if (totalEl) {
        totalEl.textContent = '$' + data.cart_total;
    }

    // Update dropdown product list
    const listEl = document.getElementById('headerCartProducts');
    if (listEl) {
        if (!data.cart_data || Object.keys(data.cart_data).length === 0) {
            listEl.innerHTML = `
                <div class="p-4 text-center text-muted" id="headerEmptyNotice" style="font-size: 1.3rem;">
                    <i class="icon-shopping-cart d-block mb-2" style="font-size: 2.5rem; opacity: 0.35;"></i>
                    Your cart is empty.
                </div>
            `;
        } else {
            let html = '';
            for (const pid in data.cart_data) {
                const item = data.cart_data[pid];
                const imgHtml = item.image
                    ? `<img src="${item.image}" alt="${item.title}" style="width: 60px; height: 60px; object-fit: contain; padding: 2px;">`
                    : `<img src="/static/assets/images/demos/demo-13/products/product-1.jpg" alt="${item.title}" style="width: 60px; height: 60px; object-fit: contain; padding: 2px;">`;

                html += `
                    <div class="product header-cart-item" id="header-cart-item-${pid}">
                        <div class="product-cart-details">
                            <h4 class="product-title">
                                <a href="/product/${pid}/">${item.title}</a>
                            </h4>
                            <span class="cart-product-info">
                                <span class="cart-product-qty">${item.qty}</span>
                                x $${item.price}
                            </span>
                        </div>
                        <figure class="product-image-container">
                            <a href="/product/${pid}/" class="product-image">
                                ${imgHtml}
                            </a>
                        </figure>
                        <a href="javascript:void(0);" class="btn-remove header-cart-remove" data-pid="${pid}" title="Remove Product">
                            <i class="icon-close"></i>
                        </a>
                    </div>
                `;
            }
            listEl.innerHTML = html;
        }
    }
}

$(document).ready(function() {
    // 1. Universal Add to Cart click handler
    $(document).on('click', '.btn-cart', function(e) {
        const $btn = $(this);

        // If this button is a direct link to the cart page itself (e.g. "View Cart"), do not intercept
        const href = $btn.attr('href');
        if (href && (href.indexOf('/cart/') !== -1 || href === '/cart/')) {
            return;
        }

        e.preventDefault();

        // Find PID
        let pid = $btn.data('pid') || $btn.attr('data-pid');
        if (!pid) {
            // Check closest product card
            const $productWrapper = $btn.closest('.product');
            if ($productWrapper.length) {
                const $detailLink = $productWrapper.find("a[href*='/product/']").first();
                if ($detailLink.length) {
                    const linkHref = $detailLink.attr('href');
                    const match = linkHref.match(/\/product\/([^\/]+)\//);
                    if (match && match[1]) {
                        pid = match[1];
                    }
                }
            }
        }

        if (!pid) {
            console.error("Could not find product PID for Add to Cart button.");
            return;
        }

        // Determine quantity:
        // If inside product-details-action and #qty is present, read #qty
        let qty = 1;
        if ($btn.closest('.product-details-action').length || $btn.attr('id') === 'add-to-cart-btn') {
            const $qtyInput = $('#qty');
            if ($qtyInput.length) {
                qty = parseInt($qtyInput.val()) || 1;
            }
        }

        const originalHtml = $btn.html();
        $btn.addClass('disabled').css('pointer-events', 'none');
        $btn.html('<span>Adding...</span>');

        const csrfToken = getCookie('csrftoken') || $('input[name="csrfmiddlewaretoken"]').val() || '';

        $.ajax({
            url: '/add-to-cart/',
            type: 'POST',
            data: {
                id: pid,
                qty: qty,
                csrfmiddlewaretoken: csrfToken
            },
            dataType: 'json',
            success: function(response) {
                if (response.status === 'success') {
                    $btn.html('<span>✓ Added!</span>');
                    $btn.css('background-color', '#28a745').css('border-color', '#28a745');
                    
                    updateHeaderCartUI(response);
                    showCartToast(response.message || 'Product added to cart!', 'success');

                    setTimeout(function() {
                        $btn.html(originalHtml);
                        $btn.removeClass('disabled').css('pointer-events', '').css('background-color', '').css('border-color', '');
                    }, 1600);
                } else {
                    $btn.html(originalHtml);
                    $btn.removeClass('disabled').css('pointer-events', '');
                    showCartToast(response.message || 'Could not add to cart.', 'error');
                }
            },
            error: function(xhr, status, error) {
                $btn.html(originalHtml);
                $btn.removeClass('disabled').css('pointer-events', '');
                showCartToast('Error adding to cart. Please try again.', 'error');
                console.error("Add to cart AJAX error:", error);
            }
        });
    });

    // 2. Header Cart Remove click handler
    $(document).on('click', '.header-cart-remove', function(e) {
        e.preventDefault();
        const $removeBtn = $(this);
        const pid = $removeBtn.data('pid');
        if (!pid) return;

        const csrfToken = getCookie('csrftoken') || $('input[name="csrfmiddlewaretoken"]').val() || '';

        $.ajax({
            url: '/delete-from-cart/',
            type: 'POST',
            data: {
                id: pid,
                csrfmiddlewaretoken: csrfToken
            },
            dataType: 'json',
            success: function(response) {
                if (response.status === 'success') {
                    updateHeaderCartUI(response);
                    showCartToast('Item removed from cart.', 'success');

                    // If on /cart/ page, update cart table row too
                    const $cartRow = $('#cart-item-row-' + pid);
                    if ($cartRow.length) {
                        $cartRow.fadeOut(300, function() {
                            $(this).remove();
                            if (response.cart_count === 0) {
                                $('#cartFilledSection').hide();
                                $('#cartEmptySection').fadeIn(300);
                            }
                        });
                        $('#cartPageSubtotal').text('$' + response.cart_total);
                        $('#cartPageTotal').text('$' + response.cart_total);
                    }
                }
            },
            error: function(xhr, status, error) {
                showCartToast('Error removing item.', 'error');
            }
        });
    });
});
