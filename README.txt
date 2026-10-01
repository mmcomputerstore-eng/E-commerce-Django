================================================================================
  MUBEEN STORE - FULL-STACK DJANGO E-COMMERCE PLATFORM
  Portfolio Project | Python Back-End Development Internship Showcase
================================================================================

PROJECT STATUS: [UNDER ACTIVE DEVELOPMENT]
DEVELOPER:      Mubeen
TARGET ROLE:    Python / Django Back-End Developer Intern
REPOSITORY:     ecomdjango
TECHNOLOGIES:   Python 3.12, Django 6.x, SQLite, Django ORM, AJAX, JavaScript, 
                Bootstrap 4, Django Jazzmin, HTML5/CSS3


================================================================================
1. PROJECT OVERVIEW
================================================================================
Mubeen Store is a robust, modular, full-stack eCommerce web application built 
with Python and Django. Designed as a flagship portfolio project for applying 
to Python Back-End Development internships, it highlights practical mastery of:

- Relational database schema design and complex ORM queries.
- Asynchronous client-server communication using AJAX and JSON responses.
- Session-based state management (dynamic shopping cart without DB overhead).
- Custom authentication, user profiles, and session security.
- Comprehensive customer dashboard with order lifecycle tracking and address book.
- Clean Model-View-Template (MVT) architecture following Django best practices.


================================================================================
2. KEY HIGHLIGHTS & ARCHITECTURAL STRENGTHS
================================================================================

[+] Custom User Model:
    Implemented a custom user model extending 'AbstractUser' with unique email 
    authentication (USERNAME_FIELD = 'email'), profile bios, and full name support.

[+] Complex Data Relationships:
    Designed schema supporting multi-vendor stores, categorized cataloging, 
    tagged products (django-taggit), product image galleries, user reviews with 
    aggregate star ratings, and order history preservation.

[+] Asynchronous AJAX Interactivity:
    Smooth user experience for cart operations (add, quantity update, remove), 
    saved address switching, address deletion, and instant order tracking modals 
    without full page reloads.

[+] Database Query Optimization:
    Used 'prefetch_related', 'annotate', 'Avg', and 'Count' aggregations to 
    eliminate N+1 query bottlenecks on catalog listings and dashboard analytics.

[+] Session-Based Shopping Cart:
    Stateful shopping cart implemented cleanly using Django sessions, ensuring 
    fast client response times and minimal database write operations before checkout.

[+] Fully Functional Customer Dashboard:
    Centralized account hub providing live metrics (Total Orders, In Process, 
    Shipped, Delivered, Total Spent), interactive order tracking timeline, full 
    printable receipts, complete address management (CRUD), and profile security.


================================================================================
3. SYSTEM ARCHITECTURE & TECH STACK
================================================================================

Back-End:
  - Language:            Python 3.12
  - Framework:           Django 6.1.1
  - ORM:                 Django ORM (Aggregations, Annotations, Prefetching)
  - Identifiers:         ShortUUID (Secure, URL-friendly unique IDs for products/vendors)
  - Tagging Engine:      django-taggit (Categorization & SEO tags)
  - Rich Text Editor:    django-ckeditor (Vendor profiles & product specs)
  - Admin Interface:     django-jazzmin (Sleek, customizable dashboard for staff)

Database:
  - Development:         SQLite3 (Engineered with standard Django ORM migrations;
                         100% compatible with PostgreSQL and MySQL for production)

Front-End & UI:
  - Templates:           Django Template Language (DTL) with partial modularization
  - Styling:             Bootstrap 4, Custom Vanilla CSS, Font Icons
  - Scripting:           JavaScript (ES6+), jQuery, AJAX (Fetch & $.ajax)
  - Feedback/UX:         Custom Toast notifications, real-time status steppers

Security & Standards:
  - CSRF Token verification on all POST/AJAX requests
  - Password hashing via Django PBKDF2 with SHA-256
  - Session auth hash updating on password change (preventing unwanted logouts)
  - Server-side data validation and sanitization


================================================================================
4. DATABASE MODELS & SCHEMA BREAKDOWN
================================================================================

1. User (userauth.models.User):
   - Extends 'AbstractUser'
   - Fields: email (unique, login identifier), username, bio, first_name, last_name
   - Authentication backend configured for email credentials.

2. Category (core.models.Category):
   - Categorizes catalog items with ShortUUID primary identifier and category image.

3. Vendor (core.models.Vendor):
   - Multi-vendor profile with cover image, rich text description, contact details, 
     shipping rating, warranty, and return policies.

4. Products (core.models.Products):
   - Main catalog item model linked to Vendor and Category.
   - Fields: pid (ShortUUID), title, image, description, price, old_price, 
     specifications, stock_count, product_status, in_stock, featured, sku.
   - Methods: avg_rating(), get_review_count() with aggregate caching.

5. ProductImage (core.models.ProductImage):
   - One-to-Many gallery images linked to a single product.

6. ProductReview (core.models.ProductReview):
   - Ratings (1 to 5 stars) and feedback text linked to User and Product.

7. CartOrders & CartOrdersItems (core.models.CartOrders, CartOrdersItems):
   - Order Header: user, price, paid_status, order_date, product_status 
     ('processing', 'shipped', 'delivered').
   - Order Items: historical snapshot preserving item title, quantity, price, 
     and line total at the moment of order placement.

8. Address (core.models.Address):
   - Multi-address storage per customer with boolean 'status' representing 
     the active default delivery address.

9. Wishlist (core.models.Wishlist):
   - Allows users to bookmark favorite products for later purchase.


================================================================================
5. CORE MODULES & FEATURES
================================================================================

A. AUTHENTICATION & PROFILE SYSTEM ('userauth')
   - User Registration with instant client & server validation.
   - Secure login via email and password.
   - Customer profile update (First Name, Last Name, Bio/Notes).
   - In-dashboard Password Change with current password validation and 
     session preservation via 'update_session_auth_hash'.

B. SHOP & CATALOG ENGINE ('core')
   - Featured products and dynamic banner displays on home page.
   - Comprehensive product catalog with multi-criteria filtering:
     * Filter by Category
     * Filter by Vendor
     * Filter by Price Range slider
     * Filter by Tags
   - Product details view with multi-image gallery, vendor credentials, 
     detailed specifications, and verified customer reviews.
   - Real-time search query processor with category filtering.

C. SHOPPING CART ('core/views.py' session engine)
   - Stateful shopping cart stored in 'request.session["cart_data_obj"]'.
   - Add to cart with custom quantity.
   - Asynchronous update of quantities and line-item totals.
   - Instant item removal with recalculation of cart badge and subtotal.
   - Global cart context processor ('core.context_processor.default') 
     providing cart count and totals on every page.

D. CHECKOUT & ORDER PIPELINE
   - Address selector displaying all saved user delivery addresses.
   - Quick address creation directly from the checkout screen.
   - Cash on Delivery (COD) processing with instant order creation.
   - Automatic generation of 'CartOrders' and child 'CartOrdersItems'.
   - Automatic session cart flushing after order completion.
   - Order completed confirmation page with summary and receipt.

E. CUSTOMER DASHBOARD ('/dashboard/')
   - Real-time Analytics:
     * Total Orders Count
     * In-Process Orders Count
     * Shipped Orders Count
     * Delivered Orders Count
     * Total Amount Spent ($)
   - Live Order Tracking Stepper in AJAX Modal:
     * Visual 4-step progress line: [Placed] -> [Processing] -> [Shipped] -> [Delivered]
     * Dynamic color-coded progression based on actual order status.
     * Itemized product breakdown with quantities and prices.
     * Direct link to full printable invoice receipt.
   - Filterable Order History Tabs:
     * View All, In Process, Shipped, or Delivered orders with live badges.
   - Delivery Address Book:
     * Highlighted active shipping address with 'DEFAULT' badge.
     * Set As Active button (instant AJAX update across dashboard and checkout).
     * Delete Address button (instant AJAX removal with automatic active address 
       re-assignment if active address is deleted).
     * Add new delivery address form.

F. WISHLIST MANAGEMENT ('/wishlist/')
   - Asynchronous Add to Wishlist from any product card or detail page.
   - Real-time global wishlist badge counter in header.
   - Dedicated Wishlist page displaying saved products, prices, and stock status.
   - Instant 1-click 'Add to Cart' directly from the wishlist table.
   - AJAX 'Remove from Wishlist' with smooth animated row removal.
   - Empty state view encouraging users to discover new products.


================================================================================
6. PROJECT DIRECTORY STRUCTURE
================================================================================

ecomdjango/
│
├── core/                        # Core eCommerce Application
│   ├── admin.py                 # Custom ModelAdmin & TabularInlines
│   ├── apps.py                  # App configuration
│   ├── context_processor.py     # Global categories, tags & cart context
│   ├── forms.py                 # ProductReview and form validation
│   ├── models.py                # Category, Vendor, Products, Orders, Address
│   ├── urls.py                  # Core route definitions
│   └── views.py                 # Views for catalog, cart, checkout, dashboard
│
├── userauth/                    # Authentication Application
│   ├── admin.py                 # Custom UserAdmin
│   ├── models.py                # Custom User model
│   ├── urls.py                  # Auth routes (sign-in, sign-up, sign-out)
│   └── views.py                 # Auth handling and session authentication
│
├── ecomdjango/                  # Project Configuration
│   ├── settings.py              # Installed apps, middleware, database, templates
│   ├── urls.py                  # Root URL dispatcher
│   └── wsgi.py                  # WSGI entry point
│
├── templates/                   # Frontend Templates (DTL)
│   ├── core/                    # Core templates
│   │   ├── dashboard.html       # Customer dashboard & order tracker
│   │   ├── cart.html            # Shopping cart interface
│   │   ├── checkout.html        # Checkout & address selection
│   │   ├── index.html           # Home page
│   │   ├── product_details.html # Product detail & review form
│   │   ├── product_list.html    # Filterable products catalog
│   │   ├── order_detail.html    # Full printable order receipt
│   │   ├── wishlist.html        # Interactive wishlist interface
│   │   └── partials/            # Reusable table partials
│   ├── partials/                # Global layout templates (base.html, header, footer)
│   └── userauth/                # Login & registration templates
│
├── staticfiles/                 # Static assets (CSS, JS, fonts, images)
│   └── assets/js/cart.js        # AJAX cart & toast notification engine
│
├── media/                       # Uploaded media (products, categories, vendors)
├── manage.py                    # Django management script
├── db.sqlite3                   # Relational database file
└── README.txt                   # Project documentation


================================================================================
7. LOCAL INSTALLATION & SETUP GUIDE
================================================================================

Prerequisites:
  - Python 3.10+ (Python 3.12 recommended)
  - pip (Python package manager)
  - virtualenv or python3-venv

Step 1: Clone or Navigate to the Project Root:
  $ cd /path/to/ecomdjango

Step 2: Create and Activate Virtual Environment:
  $ python3 -m venv .venv
  $ source .venv/bin/activate       # On Linux/macOS
  # .venv\Scripts\activate          # On Windows

Step 3: Install Required Dependencies:
  $ pip install -r requirements.txt
  (or manually: pip install django django-taggit django-ckeditor django-jazzmin pillow shortuuid)

Step 4: Configure Environment Variables:
  $ cp .env.example .env
  # Adjust SECRET_KEY, DEBUG, and ALLOWED_HOSTS in .env as needed

Step 5: Run Database Migrations:
  $ python manage.py makemigrations
  $ python manage.py migrate

Step 6: Create a Superuser Account:
  $ python manage.py createsuperuser

Step 7: Start the Development Server:
  $ python manage.py runserver 127.0.0.1:8000

Step 8: Access the Application:
  - Storefront:         http://127.0.0.1:8000/
  - Customer Dashboard: http://127.0.0.1:8000/dashboard/
  - Admin Portal:       http://127.0.0.1:8000/admin/


================================================================================
8. PRIMARY API & ROUTE REFERENCE
================================================================================

Route Pattern                         Method   Description
--------------------------------------------------------------------------------
/                                     GET      Storefront homepage
/products/                            GET      Filterable products catalog
/product/<pid>/                       GET      Product details view
/search/                              GET      Search products by keyword & category
/cart/                                GET      Shopping cart view
/add-to-cart/                         POST     AJAX endpoint to add item to cart
/update-cart/                         POST     AJAX endpoint to update item quantity
/delete-from-cart/                    POST     AJAX endpoint to remove item from cart
/clear-cart/                          POST     AJAX endpoint to empty cart
/checkout/                            GET      Order checkout & address selection
/checkout/save-address/               POST     AJAX endpoint to create delivery address
/checkout/make-default-address/       POST     AJAX endpoint to set active address
/order-completed/<oid>/               GET      Order confirmed receipt page
/dashboard/                           GET/POST Customer dashboard & profile manager
/dashboard/delete-address/            POST     AJAX endpoint to delete address
/order-detail/<oid>/                  GET      Full printable order invoice
/ajax-order-detail/<oid>/             GET      AJAX endpoint for order tracker modal
/wishlist/                            GET      Customer wishlist page
/add-to-wishlist/                     POST     AJAX endpoint to add product to wishlist
/remove-from-wishlist/                POST     AJAX endpoint to remove item from wishlist
/users/sign-in/                       GET/POST User authentication login
/users/sign-up/                       GET/POST User account registration
/users/sign-out/                      GET      User logout and session cleanup


================================================================================
9. PLANNED ROADMAP (NEXT ITERATIONS)
================================================================================

[ ] Payment Gateway Integration:
    Integrate Stripe API and PayPal SDK for automated electronic card payments 
    and webhooks.

[ ] Background Task Queue:
    Implement Celery with Redis broker for asynchronous order confirmation emails, 
    invoice PDF generation, and automated inventory notifications.

[ ] RESTful API with Django REST Framework (DRF):
    Build token-authenticated API endpoints (JWT) to allow cross-platform 
    mobile app integration.

[ ] Automated Test Suite:
    Comprehensive unit and integration test coverage using pytest-django 
    for views, models, forms, and session persistence.

[ ] Containerization & CI/CD:
    Dockerize application with Docker Compose (Django + PostgreSQL + Redis + Nginx) 
    and set up GitHub Actions CI pipeline.


================================================================================
10. DEVELOPER CONTACT & PORTFOLIO
================================================================================

Developer:       Mubeen Ahmad
Role / Focus:    Python / Django Back-End Developer
Portfolio Note:  This project reflects my practical dedication to writing clean, 
                 maintainable, and secure back-end code using Django. I am actively 
                 seeking an internship opportunity where I can contribute to 
                 production-grade Python systems, collaborate with engineering 
                 teams, and continue expanding my back-end engineering skills.

Contact / Links:
  - GitHub:      https://github.com/
  - LinkedIn:    https://linkedin.com/in/
  - Email:       mubeen@example.com

--------------------------------------------------------------------------------
Copyright (c) 2026 Mubeen Store. Developed with Python & Django.
================================================================================
