from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib import messages
from theatre.models import *
from django.urls import reverse
from theatre.models import *
from .models import *
from admin_dashboard.models import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import razorpay
from django.db.models import Q
import json
from datetime import date
from django.http import JsonResponse
from Book_my_show.settings import KEY, SECRET, account_sid, auth_token, whatsapp_number
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.core.paginator import Paginator


# Create your views here.


def home(request):
    if "admin" in request.session:
        return redirect("admin_home")
    if "theatre" in request.session:
        return redirect("theatre_home")
    if request.method == "POST":
        if "login-submit" in request.POST:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                try:
                    profile = UserProfile.objects.get(user=user)
                except UserProfile.DoesNotExist:
                    profile = None
                if profile is not None and profile.is_theatre:
                    request.session["theatre"] = username
                    login(request, user)
                    return redirect(reverse("theatre_home"))
                else:
                    login(request, user)
                    if user.is_superuser:
                        request.session["admin"] = username
                        return redirect(reverse("admin_home"))
                    else:
                        request.session["user"] = username
                        return redirect(reverse("home"))
            else:
                messages.info(request, "Invalid username or password")
                return redirect("home")
        elif "signup-submit" in request.POST:
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            username = request.POST["username"]
            email = request.POST["email"]
            phone = request.POST["phone"]
            password = request.POST["password"]
            is_theatre = request.POST.get("type") == "theatre"
            if " " in username:
                messages.info(request, "Username cannot contain white spaces")
                return redirect("home")
            if User.objects.filter(username=username).exists():
                messages.info(request, "username is taken")
                return redirect("home")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email is taken")
                return redirect("home")
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                profile = UserProfile(user=user, is_theatre=is_theatre, phone=phone)
                profile.save()

                messages.success(
                    request, "Your account has been created. Please log in."
                )
                return redirect("home")
    movies = Movies.objects.all()
    banners = Movies.objects.all()[:4]
    now_playing = Movies.objects.all()[:3]
    current_date = date.today()
    coming_soon = Movies.objects.filter(Q(release_date__gte=current_date))[:3]
    last_five_movies = Movies.objects.all()[:7]
    context = {
        "movies": movies,
        "banners": banners,
        "now": now_playing,
        "coming_soon": coming_soon,
        "last_five_movies": last_five_movies,
    }
    return render(request, "home/home.html", context)


def search(request):
    if request.method == "POST":
        search_query = request.POST.get("search_query")
        mov = Movies.objects.filter(title__icontains=search_query)
        cinemas = UserProfile.objects.filter(
            user__username__icontains=search_query,
            is_theatre=True,
            user__is_active=True,
        )
        if mov:
            for i in mov:
                return movie(request, i.id)
        elif cinemas:
            for i in cinemas:
                return list_movies(request, i.id)
        else:
            return render(request, "home/page_not_fount.html")


def all_movies(request):
    movies = Movies.objects.all()
    items_per_page = 10
    paginator = Paginator(movies, items_per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "home/all_movies.html", {"movies": movies, "page": page})


def about(request):
    return render(request, "home/about.html")


def movie(request, id):
    if "admin" in request.session:
        return redirect("admin_home")
    if "theatre" in request.session:
        return redirect("theatre_home")
    if "user" in request.session:
        mov = Movies.objects.get(id=id)
        total_minutes = mov.runtime.total_seconds() // 60

        # Extract the hours and minutes
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return render(
            request, "home/movie.html", {"mov": mov, "hours": hours, "minutes": minutes}
        )
    else:
        return redirect("home")


def cinemas(request):
    if "admin" in request.session:
        return redirect("admin_home")
    if "theatre" in request.session:
        return redirect("theatre_home")
    if "user" in request.session:
        screens = Screen.objects.all()
        cinemas = UserProfile.objects.filter(
            user__is_active=True, screen__in=screens, is_theatre=True
        ).distinct()
        items_per_page = 6
        paginator = Paginator(cinemas, items_per_page)
        page_number = request.GET.get("page")
        page = paginator.get_page(page_number)
        return render(request, "home/cinemas.html", {"cinemas": cinemas, "page": page})
    else:
        return redirect("home")


def list_movies(request, id):
    if "admin" in request.session:
        return redirect("admin_home")
    if "theatre" in request.session:
        return redirect("theatre_home")
    if "user" in request.session:
        current_date = timezone.now().date()
        upto_six = current_date + timedelta(days=5)
        date_range = []
        while current_date <= upto_six:
            date_range.append(current_date)
            current_date += timedelta(days=1)
        screens = Screen.objects.filter(theatre=id)
        items_per_page = 3
        paginator = Paginator(screens, items_per_page)
        page_number = request.GET.get("page")
        page = paginator.get_page(page_number)
        return render(
            request,
            "home/list_movies.html",
            {"screens": screens, "date_range": date_range, "page": page},
        )
    else:
        return redirect("home")


def theatre_choose(request, id):
    if "admin" in request.session:
        return redirect("admin_home")
    if "theatre" in request.session:
        return redirect("theatre_home")
    if "user" in request.session:
        mov = Movies.objects.get(id=id)
        current_date = timezone.now().date()
        upto_six = current_date + timedelta(days=5)
        date_range = []
        while current_date <= upto_six:
            date_range.append(current_date)
            current_date += timedelta(days=1)
        theatre = Screen.objects.filter(movies_id=id, theatre__user__is_active=True)
        items_per_page = 5
        paginator = Paginator(theatre, items_per_page)
        page_number = request.GET.get("page")
        page = paginator.get_page(page_number)
        return render(
            request,
            "home/theatre_choose.html",
            {"mov": mov, "theatres": theatre, "date_range": date_range, "page": page},
        )
    else:
        return redirect("home")


def seat_selection(request, theatre_id, screen_id, show_time_id, selected_date):
    if "admin" in request.session:
        return redirect("admin_home")
    if "theatre" in request.session:
        return redirect("theatre_home")
    if "user" in request.session:
        screens = Screen.objects.get(id=screen_id)
        global screen_id_selected
        screen_id_selected = screen_id
        show_time = Show_Time.objects.get(id=show_time_id)
        selected_date = selected_date
        date = datetime.strptime(selected_date, "%Y-%m-%d")
        formatted_date = date.strftime("%b %d")
        print(
            "screen:",
            screens.name,
            "theatre:",
            screens.theatre.user.username,
            "screen_id_selected:",
            screen_id_selected,
            "date:",
            formatted_date,
            "show_time:",
            show_time,
        )
        bookseats = BookedSeat.objects.filter(
            screen=screens.name,
            theatre=screens.theatre.user.username,
            date=formatted_date,
            show_time=show_time,
        )
        booked_seats_list = []  # Create a new list to store booked seats
        for bookseat in bookseats:
            seats = bookseat.booked_seats.split(
                ", "
            )  # Split the string by comma and space
            seats = [
                seat.strip("'") for seat in seats
            ]  # Remove single quotes from each seat
            booked_seats_list.extend(seats)
        print(booked_seats_list)
        # print('screen_id',screen_id_selected)
        context = {
            "theatres": screens,
            "times": show_time,
            "selected_date": formatted_date,
            "screen_id": screens,
            "rows": screens.total_seat_rows,
            "columns": screens.total_seat_columns,
            "bookseat": booked_seats_list,
        }
        if request.method == "POST":
            selected_seats_str = request.POST.get("seats")
            print("in seat selection")
            print("selected_seats_str", selected_seats_str)
            selected_seats = selected_seats_str.split(",") if selected_seats_str else []
            print("selected_seats:", selected_seats)
            theatre = request.POST.get("theatre_name")
            screen = request.POST.get("screen_name")
            movie_title = request.POST.get("movie_title")
            time = request.POST.get("time")
            selected_date = request.POST.get("selected_date")
            seat_count = len(selected_seats)
            price_str = request.POST.get("total_price")
            price = float(price_str)
            # print('price type',type(price))
            screen_id = request.POST.get("screen_id")
            print("screen_id", screen_id_selected)
            total_price = price * seat_count
            tax = 42.00
            grand_total = total_price + tax
            theatre_details = UserProfile.objects.get(user__username=theatre)
            items = {
                "selected_seats": selected_seats,
                "theatre": theatre,
                "screen": screen,
                "movie_title": movie_title,
                "time": time,
                "selected_date": selected_date,
                "seat_count": seat_count,
                "total_price": total_price,
                "grand_total": grand_total,
                "api_key": KEY,
                "theatre_details": theatre_details,
            }
            return render(request, "home/payment.html", items)
        else:
            return render(request, "home/seat_selection.html", context)
    else:
        return redirect("home")


client = razorpay.Client(auth=(KEY, SECRET))
client_twilio = Client(account_sid, auth_token)


@csrf_exempt
def payment(request):
    if "admin" in request.session:
        return redirect("admin_home")
    if "theatre" in request.session:
        return redirect("theatre_home")
    if "user" in request.session:
        payment_order_id = None
        razorpay_payment_id = None

        DATA = {
            "amount": 5000,
            "currency": "INR",
            "receipt": "receipt#1",
            "payment_capture": "1",
        }
        payment_order = client.order.create(data=DATA)
        payment_order_id = payment_order["id"]
        context = {
            "api_key": KEY,
            "razorpay_payment_id": razorpay_payment_id,
            "order_id": payment_order_id,
        }
        if request.method == "POST":
            try:
                razorpay_payment_id = request.POST.get("razorpay_payment_id")
                selected_seats_list = request.POST.get("selected_seats")
                selected_seats = str(selected_seats_list)[1:-1]
                formatted_seats = ", ".join(selected_seats.replace("'", "").split(", "))
                print("selected_seats", selected_seats)
                theatre = request.POST.get("theatre_name")
                screen = request.POST.get("screen_name")
                movie_title = request.POST.get("movie_title")
                email = request.POST.get("email")
                mobile = request.POST.get("mobile")
                time = request.POST.get("time")
                selected_date = request.POST.get("selected_date")
                payment_id = payment_order_id
                print("payment_id", payment_id)
                seat_list = [seat.strip("' ") for seat in selected_seats.split(",")]
                seat_count = len(seat_list)
                print("seat_count", seat_count)
                price_str = request.POST.get("total_price")
                price = float(price_str)
                screen_id = request.POST.get("screen_id")
                total_price = 0
                grand_total = 0
                total_price = price
                tax = 42.00
                grand_total = total_price + tax
                screen_id = Screen.objects.get(id=screen_id_selected)
                screen = Screen.objects.get(id=screen_id_selected)
                screen_name = screen.name.split(" - ")[0]
                movie = Movies.objects.get(title=movie_title)
                movie_poster = movie.image
                print("api_key:", KEY)
                booked = BookedSeat(
                    screen=screen_name,
                    user=request.user,
                    email=email,
                    movie=movie_title,
                    movie_poster=movie_poster,
                    phone=mobile,
                    theatre=theatre,
                    booked_seats=selected_seats,
                    count=seat_count,
                    price=grand_total,
                    date=selected_date,
                    show_time=time,
                    payment_order_id=payment_order_id,
                    payment_id=razorpay_payment_id,
                )
                booked.save()
                request.session["payment_id"] = payment_id
                theatre_price = Decimal(grand_total)
                theatre_earnings = theatre_price * Decimal("0.85")
                admin_earnings = theatre_price * Decimal("0.15")
                theatre_sale_report = Theatre_Sale_Report(
                    name=theatre, booking=booked, theatre_earnings=theatre_earnings
                )
                theatre_sale_report.save()

                superuser = User.objects.get(is_superuser=True)
                admin_sale_report = Admin_Sale_Report(
                    name=superuser,
                    theatre_sale_report=theatre_sale_report,
                    admin_earnings=admin_earnings,
                )
                admin_sale_report.save()

                booked_details = BookedSeat.objects.get(
                    payment_order_id=payment_order_id
                )
                subject = "Booking Confirmation"
                message = (
                    f"Thank you for your payment. Your booking has been confirmed.\n\n"
                )
                message += f"Booking Details:\n"
                message += f"Booking ID: {booked_details.booking_id}\n"
                message += f"Movie: {booked_details.movie}\n"
                message += f"Screen: {booked_details.screen}\n"
                message += f"Theatre: {booked_details.theatre}\n"
                message += f"Booked Seats: {booked_details.booked_seats}\n"
                message += f"Total Seats: {booked_details.count}\n"
                message += f"Price: {booked_details.price}\n"
                message += f"Date: {booked_details.date}\n"
                message += f"Time: {booked_details.show_time}\n"
                message += f"Payment ID: {booked_details.payment_id}\n"
                message += "\nThank you for choosing our service. Enjoy the show!"
                email_host_user = settings.EMAIL_HOST_USER
                from_email = email_host_user
                recipient_list = [booked_details.email]
                recipient_mobile = [booked_details.phone]
                recipient_mobile = [f"+91{number}" for number in recipient_mobile]
                recipient_mobile = ",".join(recipient_mobile)
                print(
                    "after payment emai:",
                    recipient_list,
                    "mobile:",
                    recipient_mobile,
                    "message:",
                    message,
                )
                send_mail(
                    subject, message, from_email, recipient_list, fail_silently=False
                )
                print("mail sended successfully")
                print(
                    "before sending whatsapp msg:",
                    whatsapp_number,
                    "mobile:",
                    recipient_mobile,
                    "message:",
                    message,
                )
                message = client_twilio.messages.create(
                    from_="whatsapp:" + whatsapp_number,
                    body=message,
                    to="whatsapp:" + recipient_mobile,
                )
                print("sms sended successfully")
                return render(
                    request,
                    "home/payment_successful.html",
                    {"booked_details": booked_details},
                )
            except TwilioRestException as e:
                # Handle Twilio exception
                error_message = str(e)
                return render(
                    request,
                    "home/payment_successful.html",
                    {"booked_details": booked_details, "error_message": error_message},
                )
            except Exception as e:
                # Handle other exceptions
                error_message = str(e)
                return render(
                    request,
                    "home/payment_successful.html",
                    {"booked_details": booked_details, "error_message": error_message},
                )
        else:
            return render(request, "home/payment.html", context)
    else:
        return redirect("home")


def payment_successful(request):
    if "admin" in request.session:
        return redirect("admin_home")
    if "theatre" in request.session:
        return redirect("theatre_home")
    if "user" in request.session:
        return render(request, "home/payment_successful.html")
    else:
        return redirect("home")


def user_logout(request):
    if "user" in request.session:
        request.session.flush()
    logout(request)
    return redirect("home")
