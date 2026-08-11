
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from menu.models import Fooditems
from .models import Cart,CartItem,Order,OrderItem
import uuid

@login_required
def add_to_cart(request, food_id):

    # -----------------------------------------
    # Get Food
    # -----------------------------------------

    food = get_object_or_404(

        Fooditems,

        id=food_id,

        available=True,

    )

    # -----------------------------------------
    # Get Or Create Cart
    # -----------------------------------------

    cart, created = Cart.objects.get_or_create(

        user=request.user

    )

    # -----------------------------------------
    # Quantity From Form
    # -----------------------------------------

    quantity = int(

        request.POST.get(

            "quantity",

            1

        )

    )

    # -----------------------------------------
    # Check Existing Item
    # -----------------------------------------

    cart_item = CartItem.objects.filter(

        cart=cart,

        food=food,

    ).first()

    # -----------------------------------------
    # Increase Quantity
    # -----------------------------------------

    if cart_item:

        cart_item.quantity += quantity

        cart_item.save()

    # -----------------------------------------
    # Create New Item
    # -----------------------------------------

    else:

        CartItem.objects.create(

            cart=cart,

            food=food,

            quantity=quantity,

        )

    # -----------------------------------------
    # Success Message
    # -----------------------------------------

    messages.success(

        request,

        f"✅ {quantity} × {food.name} added to your cart."

    )

    # -----------------------------------------
    # Back To Previous Page
    # -----------------------------------------

    return redirect(

        request.META.get(

            "HTTP_REFERER",

            "menu"

        )

    )

@login_required
def buy_now(request, food_id):

    food = get_object_or_404(

        Fooditems,

        id=food_id,

        available=True,

    )

    cart, created = Cart.objects.get_or_create(

        user=request.user

    )

    quantity = int(

        request.POST.get(

            "quantity",

            1

        )

    )

    cart_item = CartItem.objects.filter(

        cart=cart,

        food=food

    ).first()

    if cart_item:

        cart_item.quantity += quantity

        cart_item.save()

    else:

        CartItem.objects.create(

            cart=cart,

            food=food,

            quantity=quantity

        )

    return redirect("checkout")

@login_required
def cart(request):

    cart, created = Cart.objects.get_or_create(

        user=request.user

    )

    cart_items = CartItem.objects.filter(

        cart=cart

    ).select_related("food")

    context = {

        "cart": cart,

        "cart_items": cart_items,

    }

    return render(

        request,

        "cart.html",

        context,

    )

@login_required
def increase_quantity(request, item_id):

    item = get_object_or_404(

        CartItem,

        id=item_id,

        cart__user=request.user

    )

    item.quantity += 1

    item.save()

    messages.success(

        request,

        f"{item.food.name} quantity increased."

    )

    return redirect("cart")

@login_required
def decrease_quantity(request, item_id):

    item = get_object_or_404(

        CartItem,

        id=item_id,

        cart__user=request.user

    )

    # -----------------------------------------
    # Decrease Quantity
    # -----------------------------------------

    if item.quantity > 1:

        item.quantity -= 1

        item.save()

        messages.info(

            request,

            f"{item.food.name} quantity decreased."

        )

    # -----------------------------------------
    # Remove Item
    # -----------------------------------------

    else:

        food_name = item.food.name

        item.delete()

        messages.warning(

            request,

            f"{food_name} removed from cart."

        )

    return redirect("cart")


@login_required
def remove_from_cart(request, item_id):

    item = get_object_or_404(

        CartItem,

        id=item_id,

        cart__user=request.user

    )

    food_name = item.food.name

    item.delete()

    messages.warning(

        request,

        f"{food_name} removed from your cart."

    )

    return redirect("cart")

@login_required
def checkout(request):

    cart = get_object_or_404(

        Cart,

        user=request.user

    )

    cart_items = cart.items.all()

    # --------------------------------------------------
    # Empty Cart
    # --------------------------------------------------

    if not cart_items.exists():

        messages.error(

            request,

            "Your cart is empty. Please add some delicious food first."

        )

        return redirect("cart")

    # --------------------------------------------------
    # Checkout
    # --------------------------------------------------

    if request.method == "POST":

        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError

        # --------------------------------------------------
        # Get Form Data
        # --------------------------------------------------

        full_name = request.POST.get(

            "full_name",

            ""

        ).strip()

        email = request.POST.get(

            "email",

            ""

        ).strip()

        phone = request.POST.get(

            "phone",

            ""

        ).strip()

        address = request.POST.get(

            "address",

            ""

        ).strip()

        landmark = request.POST.get(

            "landmark",

            ""

        ).strip()

        pincode = request.POST.get(

            "pincode",

            ""

        ).strip()

        payment_method = request.POST.get(

            "payment_method"

        )

        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

        if len(full_name) < 3:

            messages.error(

                request,

                "Please enter a valid full name."

            )

            return redirect("checkout")

        try:

            validate_email(email)

        except ValidationError:

            messages.error(

                request,

                "Please enter a valid email address."

            )

            return redirect("checkout")

        if not phone.isdigit() or len(phone) != 10:

            messages.error(

                request,

                "Phone number must contain exactly 10 digits."

            )

            return redirect("checkout")

        if not pincode.isdigit() or len(pincode) != 6:

            messages.error(

                request,

                "Pincode must contain exactly 6 digits."

            )

            return redirect("checkout")

        # --------------------------------------------------
        # Create Order
        # --------------------------------------------------

        order = Order.objects.create(

            user=request.user,

            order_number=f"FH-{uuid.uuid4().hex[:8].upper()}",

            full_name=full_name,

            email=email,

            phone=phone,

            address=address,

            landmark=landmark,

            pincode=pincode,

            subtotal=cart.total_price,

            delivery_charge=40,

            discount=0,

            grand_total=cart.grand_total,

            payment_method=payment_method,

        )

        # --------------------------------------------------
        # Copy Cart Items
        # --------------------------------------------------

        for item in cart_items:

            OrderItem.objects.create(

                order=order,

                food=item.food,

                food_name=item.food.name,

                price=item.food.price,

                quantity=item.quantity,

                subtotal=item.subtotal,

            )

        # --------------------------------------------------
        # Clear Cart
        # --------------------------------------------------

        cart_items.delete()

        messages.success(

            request,

            f"🎉 Order {order.order_number} has been placed successfully!"

        )

        return redirect(

            "order_success",

            order.id

        )

    # --------------------------------------------------
    # Context
    # --------------------------------------------------

    context = {

        "cart": cart,

        "cart_items": cart_items,

    }

    return render(

        request,

        "checkout.html",

        context

    )


@login_required
def order_success(request, order_id):

    order = get_object_or_404(

        Order,

        id=order_id,

        user=request.user,

    )

    return render(

        request,

        "order_success.html",

        {

            "order": order

        }

    )

@login_required
def order_success(request, order_id):

    order = get_object_or_404(

        Order,

        id=order_id,

        user=request.user,

    )

    context = {

        "order": order

    }

    return render(

        request,

        "order_success.html",

        context

    )

@login_required
def my_orders(request):

    orders = Order.objects.filter(

        user=request.user

    )

    context = {

        "orders": orders

    }

    return render(

        request,

        "my_orders.html",

        context

    )

@login_required
def order_detail(request, order_id):

    order = get_object_or_404(

        Order,

        id=order_id,

        user=request.user,

    )

    context = {

        "order": order

    }

    return render(

        request,

        "order_detail.html",

        context

    )


@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(

        Order,

        id=order_id,

        user=request.user,

    )

    # --------------------------------------------------
    # Check if order can be cancelled
    # --------------------------------------------------

    if order.status not in ["Pending", "Confirmed"]:

        messages.error(

            request,

            "❌ This order can no longer be cancelled."

        )

        return redirect(

            "order_detail",

            order.id

        )

    # --------------------------------------------------
    # Cancel Order
    # --------------------------------------------------

    if request.method == "POST":

        order.status = "Cancelled"

        # If payment was already made,
        # mark it as refunded for now.

        if order.payment_status == "Paid":

            order.payment_status = "Refunded"

        order.save()

        messages.success(

            request,

            f"✅ Order {order.order_number} has been cancelled."

        )

        return redirect(

            "order_detail",

            order.id

        )

    # --------------------------------------------------
    # Prevent GET cancellation
    # --------------------------------------------------

    return redirect(

        "order_detail",

        order.id

    )