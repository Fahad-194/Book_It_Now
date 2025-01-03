from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignupForm
from .models import CustomUser, UserActivity
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request,template_name='Main/Home.html')
def login(request,user):
    return render(request,template_name='Main/Log_In.html')
def main(request):
    return render(request,template_name='Main/Main.html')
def signup(request):
    return render(request,template_name='Main/Sign_Up.html')
def main(request):
    return render(request, 'Main/main.html')
def about_us(request):
    return render(request, 'Main/about_us.html')
def contact_us(request):
    return render(request, 'Main/contact_us.html')
def terms(request):
    return render(request, 'Main/terms_conditions.html')
def submit_contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Process or save the data
        return HttpResponse("Thank you for contacting us!")
    return HttpResponse("Invalid request.")

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the signup event
            UserActivity.objects.create(user=user, action='signup')
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('Log_In')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()

    return render(request, 'Main/Sign_Up.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.http import url_has_allowed_host_and_scheme
from Main.models import UserActivity


def login_view(request):
    next_url = request.GET.get('next', '')  # Capture the next parameter from the URL

    if request.method == 'POST':
        email_or_phone = request.POST.get('email_or_phone')
        password = request.POST.get('password')
        next_url = request.POST.get('next', '')  # Get the next parameter from the form

        # Authenticate the user
        user = None
        try:
            if '@' in email_or_phone:
                user = authenticate(request, username=email_or_phone, password=password)
            else:
                user = authenticate(request, username=email_or_phone, password=password)

        except Exception:
            user = None

        if user is not None:
            login(request, user)  # Log the user in
            UserActivity.objects.create(user=user, action='login')  # Log activity

            # Redirect to the next URL if it's safe, otherwise redirect to 'Main'
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('Main')
        else:
            return render(request, 'Main/Log_In.html', {
                'error': 'Invalid email, phone number, or password.',
                'next': next_url,
            })

    return render(request, 'Main/Log_In.html', {'next': next_url})


def forget_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            User = get_user_model()
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            reset_url = request.build_absolute_uri(
                reverse("reset_password", args=[user.pk, token])
            )
            subject = "Password Reset Request"
            message = render_to_string("Main/reset_password_email.html", {"reset_url": reset_url})
            send_mail(subject, message, "admin@example.com", [email])
            messages.success(request, "Password reset link has been sent to your email.")
            return redirect("forgot_password")
        except User.DoesNotExist:
            messages.error(request, "No user is associated with this email address.")
    return render(request, 'Main/forgot_password.html')


def reset_password(request, user_id, token):
    try:
        User = get_user_model()
        user = User.objects.get(pk=user_id)
        if not default_token_generator.check_token(user, token):
            messages.error(request, "The reset link is invalid or has expired.")
            return redirect("forgot_password")
        if request.method == "POST":
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password == confirm_password:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)  # Keeps the user logged in after password change
                messages.success(request, "Password has been reset successfully.")
                return redirect("Log_In")
            else:
                messages.error(request, "Passwords do not match.")
        return render(request, "Main/reset_password.html", {"user_id": user_id, "token": token})
    except User.DoesNotExist:
        messages.error(request, "Invalid user.")
        return redirect("forgot_password")