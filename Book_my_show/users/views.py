from django.shortcuts import render, redirect
from theatre.models import *
from django.http import JsonResponse
from theatre.models import *
from .models import *
from home.forms import UserProfileForm
from django.core.paginator import Paginator


# Create your views here.
def user_profile(request):
    if "admin" in request.session:
        return redirect("admin_home")
    if "theatre" in request.session:
        return redirect("theatre_home")
    if "user" in request.session:
        user = User.objects.get(username=request.user)
        user_profile = UserProfile.objects.get(user=user)
        if request.method == "POST":
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                profile_pic = form.cleaned_data["profile_image"]
                username = form.cleaned_data["username"]
                email = form.cleaned_data["email"]
                phone = form.cleaned_data["phone"]
                address = form.cleaned_data["address"]
                location = form.cleaned_data["location"]

                # Update the user details
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                # Update the user profile details
                user_profile.profile_image = profile_pic
                user_profile.phone = phone
                user_profile.address = address
                user_profile.location = location
                user_profile.save()

                return redirect("user_profile")
        else:
            user_data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
            }
            form = UserProfileForm(instance=user_profile, initial=user_data)
            return render(
                request,
                "users/user_profile.html",
                {"form": form, "user_profile": user_profile},
            )
    else:
        return redirect("home")


def update_booking_cancellation_request(booking, theatre, user, reason, status):
    (
        booking_cancellation_request,
        created,
    ) = BookingCancellationRequest.objects.get_or_create(booking=booking)
    if not created:
        booking_cancellation_request.theatre = theatre
        booking_cancellation_request.user = user
        booking_cancellation_request.reason = reason
    booking_cancellation_request.status = status
    booking_cancellation_request.save()


def bookings(request):
    user = request.user
    booking_details = BookedSeat.objects.filter(user=user).order_by("-id")
    booking_ids = booking_details.values_list("id", flat=True)
    cancel_requests = BookingCancellationRequest.objects.filter(booking__in=booking_ids)
    items_per_page = 3
    paginator = Paginator(booking_details, items_per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    if request.method == "POST":
        # Assuming you have form inputs for the booking_cancellation_request fields
        theatre = request.POST.get("theatre")
        reason = request.POST.get("reason")
        status = request.POST.get("status")

        # Assuming you have the booking object to update
        booking = BookedSeat.objects.get(id=request.POST.get("booking_id"))

        update_booking_cancellation_request(booking, theatre, user, reason, status)
    return render(
        request,
        "users/bookings.html",
        {
            "booking_details": booking_details,
            "cancel_requests": cancel_requests,
            "page": page,
        },
    )


def cancel_booking(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        booking = BookedSeat.objects.get(id=booking_id)
        theatre = booking.theatre
        reason = request.POST.get("reason")
        user = request.user
        # Check if a cancellation request already exists for the booking
        cancellation_request = BookingCancellationRequest.objects.filter(
            booking=booking
        ).first()
        if cancellation_request:
            return JsonResponse(
                {"status": "error", "message": "Cancellation request already exists."}
            )

        cancellation_request = BookingCancellationRequest.objects.create(
            booking=booking, theatre=theatre, reason=reason, status="pending", user=user
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})
