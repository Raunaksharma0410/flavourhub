from django.db import models

from django.conf import settings

from menu.models import Fooditems



# ==========================================================
#                           CART
# ==========================================================

class Cart(models.Model):

    # ------------------------------------------------------
    # Cart Owner
    # ------------------------------------------------------

    user = models.OneToOneField(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="cart"

    )

    # ------------------------------------------------------
    # Cart Created Time
    # ------------------------------------------------------

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    # ------------------------------------------------------
    # Last Updated
    # ------------------------------------------------------

    updated_at = models.DateTimeField(

        auto_now=True

    )

    # ------------------------------------------------------
    # String Representation
    # ------------------------------------------------------

    def __str__(self):

        return f"{self.user.username}'s Cart"

    # ------------------------------------------------------
    # Total Items in Cart
    # ------------------------------------------------------

    @property
    def total_items(self):

        return sum(

            item.quantity

            for item in self.items.all()

        )

    # ------------------------------------------------------
    # Cart Total Price
    # ------------------------------------------------------

    @property
    def total_price(self):

        return sum(

            item.subtotal

            for item in self.items.all()

        )

    # ------------------------------------------------------
    # Default Ordering
    # ------------------------------------------------------

    class Meta:

        ordering = ["-updated_at"]

        verbose_name = "Cart"

        verbose_name_plural = "Carts"

        # ------------------------------------------------------
        # Grand Total
        # ------------------------------------------------------

    @property
    def grand_total(self):
        delivery_charge = 40

        return self.total_price + delivery_charge


# ==========================================================
#                       CART ITEM
# ==========================================================

class CartItem(models.Model):

    # ------------------------------------------------------
    # Cart
    # ------------------------------------------------------

    cart = models.ForeignKey(

        Cart,

        on_delete=models.CASCADE,

        related_name="items"

    )

    # ------------------------------------------------------
    # Food Item
    # ------------------------------------------------------

    food = models.ForeignKey(

        Fooditems,

        on_delete=models.CASCADE,

        related_name="cart_items"

    )

    # ------------------------------------------------------
    # Quantity
    # ------------------------------------------------------

    quantity = models.PositiveIntegerField(

        default=1

    )

    # ------------------------------------------------------
    # Added Time
    # ------------------------------------------------------

    added_at = models.DateTimeField(

        auto_now_add=True

    )

    # ------------------------------------------------------
    # Last Updated
    # ------------------------------------------------------

    updated_at = models.DateTimeField(

        auto_now=True

    )

    # ------------------------------------------------------
    # Subtotal
    # ------------------------------------------------------

    @property
    def subtotal(self):

        return self.food.price * self.quantity

    # ------------------------------------------------------
    # String Representation
    # ------------------------------------------------------

    def __str__(self):

        return f"{self.quantity} x {self.food.name}"

    # ------------------------------------------------------
    # Meta Information
    # ------------------------------------------------------

    class Meta:

        ordering = ["-added_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["cart", "food"],
                name="unique_food_in_cart"
            )
        ]

        verbose_name = "Cart Item"

        verbose_name_plural = "Cart Items"


# ==========================================================
#                           ORDER
# ==========================================================

class Order(models.Model):

    # ------------------------------------------------------
    # Order Status Choices
    # ------------------------------------------------------

    STATUS_CHOICES = [

        ("Pending", "Pending"),

        ("Confirmed", "Confirmed"),

        ("Preparing", "Preparing"),

        ("Out For Delivery", "Out For Delivery"),

        ("Delivered", "Delivered"),

        ("Cancelled", "Cancelled"),

    ]

    # ------------------------------------------------------
    # Payment Method Choices
    # ------------------------------------------------------

    PAYMENT_METHOD_CHOICES = [

        ("COD", "Cash On Delivery"),

        ("ONLINE", "Online Payment"),

    ]

    # ------------------------------------------------------
    # Payment Status Choices
    # ------------------------------------------------------

    PAYMENT_STATUS_CHOICES = [

        ("Pending", "Pending"),

        ("Paid", "Paid"),

        ("Failed", "Failed"),

        ("Refunded", "Refunded"),

    ]

    # ------------------------------------------------------
    # Customer
    # ------------------------------------------------------

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="orders"

    )

    # ------------------------------------------------------
    # Order Number
    # ------------------------------------------------------

    order_number = models.CharField(

        max_length=20,

        unique=True

    )

    # ------------------------------------------------------
    # Customer Details
    # ------------------------------------------------------

    full_name = models.CharField(

        max_length=100

    )

    phone = models.CharField(

        max_length=15

    )

    email = models.EmailField()

    # ------------------------------------------------------
    # Delivery Address
    # ------------------------------------------------------

    address = models.TextField()

    # ------------------------------------------------------
    # Landmark (Optional)
    # ------------------------------------------------------

    landmark = models.CharField(

        max_length=150,

        blank=True

    )

    pincode = models.CharField(

        max_length=10

    )

    # ------------------------------------------------------
    # Order Amount
    # ------------------------------------------------------

    subtotal = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )

    delivery_charge = models.DecimalField(

        max_digits=10,

        decimal_places=2,

        default=40

    )

    discount = models.DecimalField(

        max_digits=10,

        decimal_places=2,

        default=0

    )

    grand_total = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )

    # ------------------------------------------------------
    # Payment
    # ------------------------------------------------------

    payment_method = models.CharField(

        max_length=20,

        choices=PAYMENT_METHOD_CHOICES,

        default="COD"

    )

    payment_status = models.CharField(

        max_length=20,

        choices=PAYMENT_STATUS_CHOICES,

        default="Pending"

    )

    # ------------------------------------------------------
    # Order Status
    # ------------------------------------------------------

    status = models.CharField(

        max_length=30,

        choices=STATUS_CHOICES,

        default="Pending"

    )

    # ------------------------------------------------------
    # Customer Notes
    # ------------------------------------------------------

    notes = models.TextField(

        blank=True,

        null=True

    )

    # ------------------------------------------------------
    # Date
    # ------------------------------------------------------

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True


    )

    # ------------------------------------------------------
    # Order Summary
    # ------------------------------------------------------

    @property
    def order_summary(self):
        items = list(self.items.all())

        if len(items) <= 2:
            return ", ".join(

                f"{item.quantity}× {item.food_name}"

                for item in items

            )

        summary = ", ".join(

            f"{item.quantity}× {item.food_name}"

            for item in items[:2]

        )

        return f"{summary} +{len(items) - 2} more"

    # ------------------------------------------------------
    # String Representation
    # ------------------------------------------------------

    def __str__(self):

        return self.order_number

    # ------------------------------------------------------
    # Meta
    # ------------------------------------------------------

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Order"

        verbose_name_plural = "Orders"



# ==========================================================
#                       ORDER ITEM
# ==========================================================

class OrderItem(models.Model):

    # ------------------------------------------------------
    # Parent Order
    # ------------------------------------------------------

    order = models.ForeignKey(

        Order,

        on_delete=models.CASCADE,

        related_name="items"

    )

    # ------------------------------------------------------
    # Food Item
    # ------------------------------------------------------

    food = models.ForeignKey(

        Fooditems,

        on_delete=models.CASCADE,

        related_name="order_items"

    )

    # ------------------------------------------------------
    # Food Snapshot
    # ------------------------------------------------------

    food_name = models.CharField(

        max_length=100

    )

    # ------------------------------------------------------
    # Price At Purchase
    # ------------------------------------------------------

    price = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )

    # ------------------------------------------------------
    # Quantity
    # ------------------------------------------------------

    quantity = models.PositiveIntegerField(

        default=1

    )

    # ------------------------------------------------------
    # Subtotal
    # ------------------------------------------------------

    subtotal = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )

    # ------------------------------------------------------
    # String Representation
    # ------------------------------------------------------

    def __str__(self):

        return f"{self.food_name} × {self.quantity}"

    # ------------------------------------------------------
    # Meta
    # ------------------------------------------------------

    class Meta:

        ordering = ["id"]

        verbose_name = "Order Item"

        verbose_name_plural = "Order Items"