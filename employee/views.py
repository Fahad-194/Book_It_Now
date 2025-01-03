from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import EmployeeSignupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import BusRoutesForm
from bus.models import BusRoute
from .forms import TrainRouteForm
from train.models import TrainRoute
from air.models import AirRoute
from .forms import AirRouteForm
from launch.models import LaunchRoute
from .forms import LaunchRouteForm

def employee_signup_view(request):
    if request.method == 'POST':
        form = EmployeeSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admin account created successfully. You can now log in.')
            return redirect('employee_login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeSignupForm()

    return render(request, 'employee/employee_signup.html', {'form': form})

def employee_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')

        # Retrieve the user by username and employee_id
        User = get_user_model()
        try:
            user = User.objects.get(username=username, employee_id=employee_id)
            # Check the password
            if user.check_password(password):
                if user.is_active:
                    login(request, user)  # Log the user in
                    messages.success(request, 'You have successfully logged in.')
                    return redirect('employee_dashboard')  # Redirect to an admin dashboard or main page
                else:
                    messages.error(request, 'Your account is inactive.')
            else:
                messages.error(request, 'Invalid username, employee ID, or password.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username, employee ID, or password.')

    return render(request, 'employee/employee_login.html')

def employee_dashboard(request):
    return render(request,template_name='employee/employee_dashboard.html')
def bus_routes(request):
    routes_b = BusRoute.objects.all()
    return render(request, 'employee/bus_routes.html', {'routes': routes_b})
def train_routes(request):
    routes_t = TrainRoute.objects.all()
    return render(request, 'employee/train_routes.html', {'routes': routes_t})
def air_routes(request):
    routes_a = AirRoute.objects.all()
    return render(request, 'employee/air_routes.html', {'routes': routes_a})
def launch_routes(request):
    routes_l = LaunchRoute.objects.all()
    return render(request, 'employee/launch_routes.html', {'routes': routes_l})

@login_required
def create_bus_routes(request):
    if request.method == 'POST':
        form = BusRoutesForm(request.POST)
        if form.is_valid():
            bus_route = form.save(commit=False)
            bus_route.employee = request.user  # Link the bus route to the currently logged-in employee
            bus_route.save()  # Save the bus route
            messages.success(request, 'Bus route created successfully.')
            return redirect('bus_routes')  # Redirect to dashboard after successful creation
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BusRoutesForm()  # If GET request, show the empty form

    return render(request, 'employee/create_bus_routes.html', {'form': form})

@login_required
def update_bus_route(request, route_id):
    route = get_object_or_404(BusRoute, id=route_id)

    if request.method == 'POST':
        form = BusRoutesForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bus route updated successfully.')
            return redirect('bus_routes')  # Redirect to the dashboard or a relevant page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BusRoutesForm(instance=route)  # Pre-populate the form with the existing route data

    return render(request, 'employee/update_bus_route.html', {'form': form, 'route': route})

# Delete bus route view
@login_required
def delete_bus_route(request, route_id):
    route = get_object_or_404(BusRoute, id=route_id)

    if request.method == 'POST':
        route.delete()  # Delete the train route
        messages.success(request, 'Bus route deleted successfully.')
        return redirect('bus_routes')  # Redirect to the dashboard or a relevant page

    return render(request, 'employee/delete_bus_route.html', {'route': route})


@login_required
def create_train_routes(request):
    if request.method == 'POST':
        form = TrainRouteForm(request.POST)
        if form.is_valid():
            train_route = form.save(commit=False)
            train_route.employee = request.user  # Link the Train route to the currently logged-in employee
            train_route.save()  # Save the train route
            messages.success(request, 'Train route created successfully.')
            return redirect('train_routes')  # Redirect to dashboard after successful creation
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TrainRouteForm()  # If GET request, show the empty form

    return render(request, 'employee/create_train_route.html', {'form': form})

@login_required
def update_train_route(request, route_id):
    route = get_object_or_404(TrainRoute, id=route_id)

    if request.method == 'POST':
        form = TrainRouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            messages.success(request, 'Train route updated successfully.')
            return redirect('train_routes')  # Redirect to the dashboard or a relevant page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TrainRouteForm(instance=route)  # Pre-populate the form with the existing route data

    return render(request, 'employee/update_train_route.html', {'form': form, 'route': route})

# Delete bus route view
@login_required
def delete_train_route(request, route_id):
    route = get_object_or_404(TrainRoute, id=route_id)

    if request.method == 'POST':
        route.delete()  # Delete the train route
        messages.success(request, 'Train route deleted successfully.')
        return redirect('train_routes')  # Redirect to the dashboard or a relevant page

    return render(request, 'employee/delete_train_route.html', {'route': route})


@login_required
def create_air_routes(request):
    if request.method == 'POST':
        form = AirRouteForm(request.POST)
        if form.is_valid():
            air_route = form.save(commit=False)
            air_route.employee = request.user  # Link the Train route to the currently logged-in employee
            air_route.save()  # Save the train route
            messages.success(request, 'Air route created successfully.')
            return redirect('air_routes')  # Redirect to dashboard after successful creation
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AirRouteForm()  # If GET request, show the empty form

    return render(request, 'employee/create_air_route.html', {'form': form})

@login_required
def update_air_route(request, route_id):
    route = get_object_or_404(AirRoute, id=route_id)

    if request.method == 'POST':
        form = AirRouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            messages.success(request, 'Air route updated successfully.')
            return redirect('air_routes')  # Redirect to the dashboard or a relevant page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AirRouteForm(instance=route)  # Pre-populate the form with the existing route data

    return render(request, 'employee/update_air_route.html', {'form': form, 'route': route})

# Delete bus route view
@login_required
def delete_air_route(request, route_id):
    route = get_object_or_404(AirRoute, id=route_id)

    if request.method == 'POST':
        route.delete()  # Delete the train route
        messages.success(request, 'Train route deleted successfully.')
        return redirect('air_routes')  # Redirect to the dashboard or a relevant page

    return render(request, 'employee/delete_air_route.html', {'route': route})

@login_required
def create_launch_routes(request):
    if request.method == 'POST':
        form = LaunchRouteForm(request.POST)
        if form.is_valid():
            air_route = form.save(commit=False)
            air_route.employee = request.user  # Link the Train route to the currently logged-in employee
            air_route.save()  # Save the train route
            messages.success(request, 'Air route created successfully.')
            return redirect('launch_routes')  # Redirect to dashboard after successful creation
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LaunchRouteForm()  # If GET request, show the empty form

    return render(request, 'employee/create_launch_route.html', {'form': form})

@login_required
def update_launch_route(request, route_id):
    route = get_object_or_404(LaunchRoute, id=route_id)

    if request.method == 'POST':
        form = LaunchRouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            messages.success(request, 'Air route updated successfully.')
            return redirect('launch_routes')  # Redirect to the dashboard or a relevant page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LaunchRouteForm(instance=route)  # Pre-populate the form with the existing route data

    return render(request, 'employee/update_launch_route.html', {'form': form, 'route': route})

# Delete bus route view
@login_required
def delete_launch_route(request, route_id):
    route = get_object_or_404(LaunchRoute, id=route_id)

    if request.method == 'POST':
        route.delete()  # Delete the train route
        messages.success(request, 'Train route deleted successfully.')
        return redirect('launch_routes')  # Redirect to the dashboard or a relevant page

    return render(request, 'employee/delete_launch_route.html', {'route': route})


