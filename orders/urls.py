from django.urls import path

from . import views

urlpatterns = [

    path("add/<int:food_id>/",views.add_to_cart,name="add_to_cart",),

    path("cart/",views.cart,name="cart",),

    path( "increase/<int:item_id>/",views.increase_quantity,name="increase_quantity"),

     path( "decrease/<int:item_id>/", views.decrease_quantity,name="decrease_quantity"),

     path("remove/<int:item_id>/", views.remove_from_cart,name="remove_from_cart") ,

     path("checkout/",views.checkout,name="checkout",),


path(

    "buy-now/<int:food_id>/",

    views.buy_now,

    name="buy_now",

),


    path("success/<int:order_id>/",views.order_success,name="order_success",),

    path("success/<int:order_id>/",views.order_success,name="order_success",),
path(
    "my-orders/",
    views.my_orders,
    name="my_orders",
),

path(
    "order/<int:order_id>/",
    views.order_detail,
    name="order_detail",
),

path(
    "cancel-order/<int:order_id>/",
    views.cancel_order,
    name="cancel_order",
),


]