from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauth.models import User


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


STATUS_CHOICE = (
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)

STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('published', 'Published'),
)

RATING = (
    (1, '⭐☆☆☆☆'),
    (2, '⭐⭐☆☆☆'),
    (3, '⭐⭐⭐☆☆'),
    (4, '⭐⭐⭐⭐☆'),
    (5, '⭐⭐⭐⭐⭐'),
)


class Tags(models.Model):
    pass


class Category(models.Model):
    cid = ShortUUIDField(
        unique=True,
        length=10,
        max_length=20,
        prefix='cat',
        alphabet='abcdefgh1234567890'
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category')

    class Meta:
        verbose_name_plural = 'Categories'

    def category_image(self):
        if self.image:
            return mark_safe(
                '<img src="%s" width="50" height="50" style="object-fit:cover; border-radius:6px;" />' % self.image.url
            )
        return "No Image"

    def __str__(self):
        return self.title


class Vendor(models.Model):
    vid = ShortUUIDField(
        unique=True,
        length=10,
        max_length=20,
        prefix='ven',
        alphabet='abcdefgh1234567890'
    )

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    cover_image = models.ImageField(upload_to=user_directory_path, default=None, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    address = models.CharField(
        max_length=100,
        default='123 Main Street.'
    )
    contact = models.CharField(
        max_length=100,
        default='+1234'
    )
    chat_resp_time = models.CharField(
        max_length=100,
        default='100'
    )
    ship_on_time = models.CharField(
        max_length=100,
        default='100'
    )
    authentication = models.CharField(
        max_length=100,
        default='100'
    )
    days_return = models.CharField(
        max_length=100,
        default='100'
    )
    warranty_period = models.CharField(
        max_length=100,
        default='100'
    )

    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        verbose_name_plural = 'Vendors'

    def vendor_image(self):
        if self.image:
            return mark_safe(
                '<img src="%s" width="50" height="50" style="object-fit:cover; border-radius:6px;" />' % self.image.url
            )
        return "No Image"

    def vendor_cover_image(self):
        if self.cover_image:
            return mark_safe(
                '<img src="%s" width="90" height="45" style="object-fit:cover; border-radius:6px;" />' % self.cover_image.url
            )
        return "No Cover"

    def __str__(self):
        return self.title


class Products(models.Model):
    pid = ShortUUIDField(
        unique=True,
        length=10,
        max_length=20,
        prefix='pro',
        alphabet='abcdefgh1234567890'
    )

    title = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to=user_directory_path,
        default='product.jpg'
    )

    description = models.TextField(
        null=True,
        blank=True,
        default='No Description'
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=99.99
    )

    old_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    specifications = models.TextField(
        null=True,
        blank=True,
        default='No Description'
    )

    tags = models.ForeignKey(
        Tags,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    product_status = models.CharField(
        choices=STATUS,
        max_length=20,
        default='in_review'
    )

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category'
    )

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    sku = ShortUUIDField(
        unique=True,
        length=5,
        max_length=10,
        prefix='sku',
        alphabet='1234567890'
    )

    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'

    def product_image(self):
        if self.image:
            return mark_safe(
                '<img src="%s" width="50" height="50" style="object-fit:cover; border-radius:6px;" />' % self.image.url
            )
        return "No Image"

    def __str__(self):
        return self.title

    def get_percentage(self):
        if self.old_price and self.old_price > 0:
            return (self.price / self.old_price) * 100
        return 0


class ProductImage(models.Model):
    images = models.ImageField(
        upload_to='product-images',
        default='product.jpg'
    )

    product = models.ForeignKey(
        Products,
        on_delete=models.SET_NULL,
        related_name='p_images',
        null=True
    )

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Images'


#################### Orders ####################
#################### Orders ####################
#################### Orders ####################

class CartOrders(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=99.99
    )

    paid_status = models.BooleanField(default=False)

    order_date = models.DateTimeField(auto_now_add=True)

    product_status = models.CharField(
        choices=STATUS_CHOICE,
        max_length=30,
        default='processing'
    )

    class Meta:
        verbose_name_plural = 'Cart Orders'


class CartOrdersItems(models.Model):
    order = models.ForeignKey(
        CartOrders,
        on_delete=models.CASCADE
    )

    product_status = models.CharField(max_length=200)

    items = models.CharField(max_length=200)

    quantity = models.IntegerField(default=0)

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=99.99
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=99.99
    )

    class Meta:
        verbose_name_plural = 'Cart Order Items'


#################### Reviews,WishList and Address ####################
#################### Reviews,WishList and Address ####################
#################### Reviews,WishList and Address ####################

class ProductReview(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    product = models.ForeignKey(
        Products,
        on_delete=models.SET_NULL,
        null=True
    )

    review = models.TextField()

    rating = models.IntegerField(
        choices=RATING,
        null=True,
        blank=True
    )

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return self.product.title if self.product else 'Review'

    def get_rating(self):
        return self.rating


class Wishlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    product = models.ForeignKey(
        Products,
        on_delete=models.SET_NULL,
        null=True
    )

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return self.product.title if self.product else 'Wishlist Item'


class Address(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    address = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Addresses'