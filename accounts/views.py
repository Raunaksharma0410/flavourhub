
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from .forms import RegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from orders.models import Order
from django.db.models import Sum


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(

                request,

                f"🎉 Welcome to FlavorHub, {user.username}!"

            )

            return redirect("home")

    else:

        form = RegisterForm()

    context = {

        "form": form

    }

    return render(

        request,

        "register.html",

        context

    )






def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(

            request,

            username=username,

            password=password

        )

        if user is not None:

            login(

                request,

                user

            )

            messages.success(

                request,

                f"👋 Welcome back, {user.username}!"

            )

            return redirect(

                "home"

            )

        else:

            messages.error(

                request,

                "❌ Invalid username or password."

            )

    return render(

        request,

        "login.html"

    )



def user_logout(request):

    logout(request)

    messages.info(

        request,

        "👋 You have been logged out successfully. See you again!"

    )

    return redirect(

        "home"

    )



@login_required
def profile(request):

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()

            profile_form.save()

            messages.success(
                request,
                "✅ Your profile has been updated successfully."
            )

            return redirect("profile")

    else:

        user_form = UserUpdateForm(
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            instance=request.user.profile
        )

        # ======================================================
        # ORDER STATISTICS
        # ======================================================

    orders = Order.objects.filter(

        user=request.user

    )

    total_orders = orders.count()

    pending_orders = orders.filter(

        status="Pending"

    ).count()

    delivered_orders = orders.filter(

        status="Delivered"

    ).count()

    total_spent = orders.aggregate(

        total=Sum("grand_total")

    )["total"] or 0

    context = {

        "user_form": user_form,

        "profile_form": profile_form,

        "total_orders": total_orders,

        "pending_orders": pending_orders,

        "delivered_orders": delivered_orders,

        "total_spent": total_spent,

    }


    return render(
        request,
        "profile.html",
        context
    )

@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "🔒 Your password has been changed successfully."
            )

            return redirect("profile")

    else:

        form = PasswordChangeForm(
            user=request.user
        )

    context = {
        "form": form
    }

    return render(
        request,
        "change_password.html",
        context
    )