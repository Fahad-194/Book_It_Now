from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import BusRoute, Booking
from django.contrib import messages
from fuzzywuzzy import fuzz
from django.http import JsonResponse
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def bus_home(request):
    routes = BusRoute.objects.all()
    return render(request, 'Bus/Bus_Home.html', {'routes': routes})

def book_ticket(request, route_id):
    route = get_object_or_404(BusRoute, id=route_id)

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        seats_booked = int(request.POST['seats'])

        # Ensure seats_booked is a positive number
        if seats_booked <= 0:
            messages.error(request, "You must book at least one seat.")
            return redirect('book_ticket', route_id=route_id)

        # Check if there are enough available seats
        if seats_booked > route.available_seats:
            messages.error(request, "Not enough seats available.")
            return redirect('book_ticket', route_id=route_id)

        # Calculate the total price
        total_price = route.price * seats_booked

        # Create the booking
        booking = Booking.objects.create(
            customer_name=name,
            customer_email=email,
            route=route,
            seats=seats_booked,
            status='reserved'  # Set the status to 'reserved' by default
        )

        # Update available seats on the route
        route.available_seats -= seats_booked
        route.save()

        # Display success message and pass booking details to the confirmation page
        messages.success(request, "Ticket booked successfully!")
        return render(request, 'Bus/ticket_confirmation.html', {
            'name': booking.customer_name,
            'email': booking.customer_email,
            'seats': booking.seats,
            'route': route,
            'total_price': total_price,
            'booking': booking
        })

    return render(request, 'Bus/book_ticket.html', {'route': route})




# This is your reservation form handler
def reserve_seat(request):
    if request.method == 'POST':
        # Capture form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        seats = request.POST.get('seats')

        # Assuming you have a Route model with a route you selected (adjust to your needs)
        route = BusRoute.objects.get(id=1)  # Example: Get the route by ID

        # Pass data to the confirmation page
        return render(request, 'ticket_confirmation.html', {
            'name': name,
            'email': email,
            'seats': seats,
            'route': route
        })

    # Show the reservation page if the method is GET
    route = Route.objects.get(id=1)  # Example: Get the route by ID
    return render(request, 'ticket_booking.html', {'route': route})


def ticket_confirmation(request, booking_id):
    """Show ticket confirmation details for a specific booking."""
    booking = get_object_or_404(Booking, id=booking_id)
    total_price = booking.route.price * booking.seats
    context = {
        'booking': booking,
        'name': request.user,
        'total_price': total_price,  # Add the total price
        'email': booking.customer_email,  # Access email from the booking object
        'route': booking.route,
    }
    return render(request, 'Bus/ticket_confirmation.html', context)

def payment_page(request, booking_id):
    # Retrieve the booking using booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        # Simulate payment processing here
        # In a real-world app, you'd integrate with a payment gateway (e.g., Stripe) to confirm payment
        # After payment is successful, update the booking's status to 'paid'

        booking.status = 'paid'  # Update status to 'paid'
        booking.save()

        # Optionally, send a success message to the user
        messages.success(request, "Payment successful! Your booking is confirmed.")

        # Redirect to a payment success page or booking confirmation page
        return render(request, 'Bus/payment_successful.html', {
            'booking': booking
        })

    return render(request, 'Bus/payment.html', {'booking': booking})


def pay_card(request, booking_id):
    # Retrieve the booking object using the booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    # Calculate the total price for the booking
    total_price = booking.route.price * booking.seats  # Adjust based on your model structure

    # Pass the booking and total_price to the template
    return render(request, 'Bus/pay_card.html', {'booking': booking, 'total_price': total_price})

def process_card_payment(request, booking_id):
    # Fetch the booking object using the booking_id
    booking = get_object_or_404(Booking, id=booking_id)
    total_price = booking.route.price * booking.seats

    if request.method == "POST":
        name = request.POST.get('name')
        amount = total_price  # Access the total_price from the booking object
        card_number = request.POST.get('card_number')

        # Basic validation checks
        if not name or not amount or not card_number:
            messages.error(request, "All fields are required.")
            return render(request, 'Bus/pay_card.html', {'booking': booking})

        # Validate card number (simple check for 16 digits)
        if len(card_number) != 16 or not card_number.isdigit():
            messages.error(request, "Invalid card number. Please enter a valid 16-digit card number.")
            return render(request, 'Bus/pay_card.html', {'booking': booking})

        try:
            if int(amount) <= 0:
                raise ValueError("Amount should be greater than zero.")

            # Update booking status to 'Paid'
            booking.status = 'Paid'  # Change the status to 'Paid'
            booking.payment_status = 'Paid'  # Ensure payment_status is also updated to 'Paid'
            booking.save()  # Save the updated booking object

            return render(request, 'Bus/payment_success.html', {
                'user_name': name,
                'amount': amount
            })

        except Exception as e:
            messages.error(request, f"Payment failed: {str(e)}")
            return render(request, 'Bus/payment_failed.html', {'error': str(e)})

    return render(request, 'Bus/pay_card.html', {'booking': booking})


# Cancellation page
def cancel_ticket(request, booking_id):
    """Cancel a ticket and update seat availability."""

    # Get the booking object by ID
    booking = get_object_or_404(Booking, id=booking_id)

    # Only allow cancellation if the booking status is not already 'paid'
    if booking.status == 'paid':
        messages.error(request, "You cannot cancel a paid ticket.")
        return redirect('booking_history')

    # Get the associated route to update available seats
    route = booking.route

    # Update the available seats on the route
    route.available_seats += booking.seats
    route.save()

    # Update booking status to 'canceled'
    booking.status = 'canceled'
    booking.save()

    # Display success message and redirect to booking history page or confirmation page
    messages.success(request, "Your ticket has been successfully canceled. The seats have been restored.")
    return render(request,'Bus/cancel_ticket.html',{booking:booking})


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(customer_email=request.user.email)

    # Calculate the total price for each booking
    for booking in bookings:
        booking.total_price = booking.route.price * booking.seats

    return render(request, 'Bus/booking_history.html', {'bookings': bookings})


from django.shortcuts import render
from .models import BusRoute
from fuzzywuzzy import fuzz

def search_bus(request):
    query = request.GET.get('query', '').strip()
    routes = BusRoute.objects.all()

    if query:
        matched_routes = []
        for route in routes:
            match_score = fuzz.partial_ratio(query.lower(), route.destination.lower())
            if match_score >= 100:
                matched_routes.append(route)

        # Pass 'query' along with the matched routes to the template
        return render(request, 'Bus/search_bus.html', {'routes': matched_routes, 'query': query})

    return render(request, 'Bus/search_bus.html', {'routes': routes, 'query': query})





