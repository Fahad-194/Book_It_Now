from django.shortcuts import render, get_object_or_404, redirect
from bus.models import BusRoute, Booking

def pay_bkash(request, booking_id):
    # Retrieve the booking object using the booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    # Calculate the total price for the booking
    total_price = booking.route.price * booking.seats  # Adjust based on your model structure

    # Pass the booking and total_price to the template
    return render(request, 'payment/pay_bkash.html', {'booking': booking, 'total_price': total_price})


def bkash_payment_process(request, booking_id):
    # Fetch the booking object using the booking_id
    booking = get_object_or_404(Booking, id=booking_id)
    total_price = booking.route.price * booking.seats

    if request.method == "POST":
        name = request.POST.get('name')
        amount = total_price
        phone_number = request.POST.get('phone_number')

        # Basic validation checks
        if not name or not phone_number:
            messages.error(request, "All fields are required.")
            return render(request, 'payment/pay_bkash.html', {'booking': booking, 'total_price': total_price})

        # Validate phone number (simple check for 11 digits)
        if len(phone_number) != 11 or not phone_number.isdigit():
            messages.error(request, "Invalid phone number. Please enter a valid 11-digit bKash number.")
            return render(request, 'payment/pay_bkash.html', {'booking': booking, 'total_price': total_price})

        try:
            if int(amount) <= 0:
                raise ValueError("Amount should be greater than zero.")

            # Update booking status to 'Paid'
            booking.status = 'Paid'
            booking.payment_status = 'Paid'
            booking.save()

            return render(request, 'Bus/payment_success.html', {
                'user_name': name,
                'amount': amount
            })

        except Exception as e:
            messages.error(request, f"Payment failed: {str(e)}")
            return render(request, 'Bus/payment_failed.html', {'error': str(e)})

    return render(request, 'payment/pay_bkash.html', {'booking': booking, 'total_price': total_price})


def pay_rocket(request, booking_id):
    # Retrieve the booking object using the booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    # Calculate the total price for the booking
    total_price = booking.route.price * booking.seats

    # Pass the booking and total_price to the template
    return render(request, 'payment/pay_rocket.html', {'booking': booking, 'total_price': total_price})


def rocket_payment_process(request, booking_id):
    # Fetch the booking object using the booking_id
    booking = get_object_or_404(Booking, id=booking_id)
    total_price = booking.route.price * booking.seats

    if request.method == "POST":
        name = request.POST.get('name')
        amount = total_price
        phone_number = request.POST.get('phone_number')

        # Basic validation checks
        if not name or not phone_number:
            messages.error(request, "All fields are required.")
            return render(request, 'payment/pay_rocket.html', {'booking': booking, 'total_price': total_price})

        # Validate phone number (simple check for 11 digits)
        if len(phone_number) != 11 or not phone_number.isdigit():
            messages.error(request, "Invalid phone number. Please enter a valid 11-digit Rocket number.")
            return render(request, 'payment/pay_rocket.html', {'booking': booking, 'total_price': total_price})

        try:
            if int(amount) <= 0:
                raise ValueError("Amount should be greater than zero.")

            # Update booking status to 'Paid'
            booking.status = 'Paid'
            booking.payment_status = 'Paid'
            booking.save()

            return render(request, 'Bus/payment_success.html', {
                'user_name': name,
                'amount': amount
            })

        except Exception as e:
            messages.error(request, f"Payment failed: {str(e)}")
            return render(request, 'Bus/payment_failed.html', {'error': str(e)})

    return render(request, 'payment/pay_rocket.html', {'booking': booking, 'total_price': total_price})
