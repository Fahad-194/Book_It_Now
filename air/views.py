from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from .models import AirRoute,AirBooking
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def air_home(request):
    routes = AirRoute.objects.all()  # Retrieve all train routes
    return render(request, 'air/air_Home.html', {'routes': routes})


def get_seat_info_air(request, route_id, seat_class):
    try:
        route = AirRoute.objects.get(id=route_id)

        if seat_class == 'economy':
            available_seats = route.economy_class
            price = route.economy_price
        elif seat_class == 'business':
            available_seats = route.business_class
            price = route.business_price
        elif seat_class == 'first_class':
            available_seats = route.first_class
            price = route.general_price
        else:
            available_seats = 0
            price = 0

        return JsonResponse({
            'available_seats': available_seats,
            'price': price
        })
    except AirRoute.DoesNotExist:
        return JsonResponse({'error': 'Route not found'}, status=404)


def book_air_ticket(request, route_id):
    route = get_object_or_404(AirRoute, id=route_id)

    # Get seat class from query parameters or default to 'ac'
    seat_class = request.GET.get('seat_class', 'economy')

    # Fetch seat info based on the seat class
    seat_info = {
        'economy': (route.economy_class, route.economy_price),
        'business': (route.business_class, route.business_price),
        'first_class': (route.first_class, route.general_price),
    }
    available_seats, price = seat_info.get(seat_class, (0, 0))

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        seat_class = request.POST['seat_class']
        seats_booked = int(request.POST['seats'])

        if seats_booked > available_seats:
            messages.error(request, "Not enough seats available.")
            return redirect('book_air_ticket', route_id=route_id)

        total_price = price * seats_booked

        # Create a new booking
        booking = AirBooking.objects.create(
            name=name,
            email=email,
            route=route,
            seat_class=seat_class,
            seats_reserved=seats_booked,
            total_price=total_price
        )

        # Update seat count
        setattr(route, f"{seat_class}_seats", available_seats - seats_booked)
        route.save()

        messages.success(request, "Ticket booked successfully!")
        return render(request, 'air/ticket_con_air.html', {
            'name': name,
            'email': email,
            'seats': seats_booked,
            'route': route,
            'seat_class': seat_class,
            'total_price': total_price,
            'booking_id': booking.id,  # Pass the booking ID to the template
        })

    context = {
        'route': route,
        'seat_class': seat_class,
        'available_seats': available_seats,
        'price': price,
    }
    return render(request, 'air/book_air_ticket.html', context)


def air_payment_page(request, booking_id):
    """Handle the payment page for train tickets."""

    # Retrieve the booking object by booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        # Simulate payment processing here
        # In a real-world application, integrate with a payment gateway like Stripe
        # After payment is successful, update the booking status to 'paid'
        booking.status = 'paid'  # Update status to 'paid'
        booking.save()

        # Send a success message to the user
        messages.success(request, "Payment successful! Your booking is confirmed.")

        # Redirect to a payment success page or booking confirmation page
        return render(request, 'Bus/payment_success.html', {'booking': booking})

    # Render the payment page for the user to view their booking details
    return render(request, 'Bus/payment.html', {'booking': booking})


def search_air(request):
    query = request.GET.get('query', '')  # Get search query from the request
    routes = AirRoute.objects.filter(destination__icontains=query)  # Filter routes based on the query
    return render(request, 'air/search_air.html', {'routes': routes, 'query': query})


def reserve_ticket(request, route_id):
    # Retrieve the route object
    route = get_object_or_404(TrainRoute, id=route_id)

    # Get the seat class from the GET parameters or fallback to default 'ac'
    seat_class = request.GET.get('seat_class', 'economy')

    # Define available seat and price info based on seat class
    # Fetch seat info based on the seat class
    seat_info = {
        'economy': (route.economy_class, route.economy_price),
        'business': (route.business_class, route.business_price),
        'first_class': (route.first_class, route.general_price),
    }
    available_seats, price = seat_info.get(seat_class, (0, 0))

    if request.method == "POST":
        # Get the booking data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        seat_class = request.POST.get('seat_class')
        seats_booked = int(request.POST.get('seats'))

        # Check if enough seats are available
        if seats_booked > available_seats:
            messages.error(request, "Not enough seats available.")
            return redirect('book_air_ticket', route_id=route_id)

        # Calculate the total price
        total_price = price * seats_booked

        # Create a new booking record in the database
        booking = AirBooking.objects.create(
            name=name,
            email=email,
            route=route,
            seat_class=seat_class,
            seats_reserved=seats_booked,
            total_price=total_price
        )

        # Update the available seat count in the TrainRoute model
        setattr(route, f"{seat_class}_seats", available_seats - seats_booked)
        route.save()

        # Success message
        messages.success(request, "Ticket booked successfully!")

        # Render the confirmation page with booking details
        return render(request, 'air/ticket_con_air.html', {
            'name': name,
            'email': email,
            'route': route,
            'seat_class': seat_class,
            'seats': seats_booked,
            'total_price': total_price,
        })

    # If the request method is not POST (maybe an error or invalid access), redirect back to booking page
    return redirect('book_air_ticket', route_id=route_id)


def air_ticket_confirmation(request, booking_id):
    """Show train ticket confirmation details for a specific booking."""
    booking = get_object_or_404(Booking, id=booking_id)

    # Fetch total_price directly from the Booking object
    total_price = booking.total_price  # The total price is already stored in the Booking model

    context = {
        'booking_id': booking_id,  # Pass booking_id to the template
        'name': booking.name,  # Get name directly from the Booking object
        'total_price': total_price,  # The total price saved in the Booking model
        'email': booking.email,  # Get email directly from the Booking object
        'route': booking.route,  # Include route information from the Booking model
        'seats': booking.seats_reserved,  # The number of reserved seats
        'seat_class': booking.seat_class,  # Seat class reserved
    }

    return render(request, 'ticket_con_air.html', context)

def cancel_air_ticket(request, booking_id):
    """Cancel a train ticket and update seat availability."""

    # Get the booking object by ID
    booking = get_object_or_404(Booking, id=booking_id)

    # Only allow cancellation if the booking status is not already 'paid'
    if booking.status == 'paid':
        messages.error(request, "You cannot cancel a paid ticket.")
        return redirect('booking_history')  # You can change this to your desired page

    # Get the associated route to update available seats
    route = booking.route

    # Update the available seats on the route for the specific seat class
    seat_class_field = f"{booking.seat_class}_seats"  # Example: 'ac_seats' or 'shovan_seats'
    available_seats = getattr(route, seat_class_field)  # Get the current number of seats available
    setattr(route, seat_class_field, available_seats + booking.seats_reserved)  # Add back the seats
    route.save()

    # Update booking status to 'canceled'
    booking.status = 'canceled'
    booking.save()

    # Display success message and redirect to booking history page or confirmation page
    messages.success(request, "Your ticket has been successfully canceled. The seats have been restored.")
    return render(request, 'bus/cancel_ticket.html', {'booking': booking})


