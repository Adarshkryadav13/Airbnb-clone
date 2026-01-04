from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from listings.models import Listing
from .models import Booking
from django.contrib import messages
import razorpay
from django.conf import settings
from datetime import datetime

@login_required
def book_room(request, id):
    listing = get_object_or_404(Listing, id=id)

    if request.method == 'POST':
        Booking.objects.create(
            user=request.user,
            listing=listing,
            check_in=request.POST['check_in'],
            check_out=request.POST['check_out']
        )
        
        messages.success(request, "Your booking has been created successfully!")
        return redirect('my_bookings')


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, id):

    booking = get_object_or_404(Booking, id=id, user=request.user)

    if request.method == 'POST':
        booking.delete()
        return redirect('my_bookings')

    return redirect('my_bookings')

@login_required
def create_payment(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    check_in = request.POST["check_in"]
    check_out = request.POST["check_out"]

    days = (
        datetime.strptime(check_out, "%Y-%m-%d")-
        datetime.strptime(check_in,"%Y-%m-%d")
    ).days

    total_price = days * listing.price_per_night

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)

    )
    order = client.order.create({
        "amount": total_price * 100,
        "currency": "INR",
        "payment_capture": 1

    })
    booking = Booking.objects.create(
        user=request.user,
        listing=listing,
        check_in=check_in,
        check_out=check_out,
        total_price=total_price,
        razorpay_order_id=order["id"]
    )
    return render(request, "payment.html", {
        "order": order,
        "booking": booking,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "listing": listing
    })

@login_required
def verify_payment(request):
    payment_id = request.GET.get("payment_id", "").strip()
    order_id = request.GET.get("order_id", "").strip()
    signature = request.GET.get("signature", "").strip()

    try:
        booking = Booking.objects.get(razorpay_order_id=order_id)
    except Booking.DoesNotExist:
        return redirect("home")  # fallback safety

    booking.razorpay_payment_id = payment_id
    booking.razorpay_signature = signature
    booking.save() 

    return render(request,"payment_success.html",{
        "bookings":booking
    })