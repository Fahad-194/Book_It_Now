from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from .forms import TravelExperienceForm
from .models import TravelExperience, Reaction, Comment
from django.http import JsonResponse
from django.contrib.auth import logout

# Create your views here.
def profile_management(request):
    return render(request,'profile/profile_management.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm

@login_required
def user_profile(request):
    return render(request, 'profile/user_profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        # Get password fields from the form
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if user_form.is_valid() and profile_form.is_valid():
            # Handle password change if it's filled
            if new_password1 or new_password2:  # Only change password if both fields are filled
                if request.user.check_password(old_password):  # Check if old password is correct
                    if new_password1 == new_password2:  # Check if new password and confirm password match
                        request.user.set_password(new_password1)  # Set the new password
                        update_session_auth_hash(request, request.user)  # Keep the user logged in after password change
                        messages.success(request, 'Password updated successfully.')
                    else:
                        messages.error(request, 'New passwords do not match.')
                else:
                    messages.error(request, 'Old password is incorrect.')

            # Save user and profile updates after handling password change
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user_profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

    return render(request, 'profile/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def share_experience(request):
    if request.method == "POST":
        form = TravelExperienceForm(request.POST, request.FILES)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            return redirect('user_forum')
    else:
        form = TravelExperienceForm()
    return render(request, 'profile/share_experience.html', {'form': form})

def user_forum(request):
    experiences = TravelExperience.objects.all().order_by('-created_at')
    return render(request, 'profile/user_forum.html', {'experiences': experiences})

@login_required
def add_reaction(request, experience_id, reaction_type):
    experience = get_object_or_404(TravelExperience, id=experience_id)
    reaction, created = Reaction.objects.get_or_create(user=request.user, experience=experience)

    if not created:
        # Update reaction if it already exists
        reaction.reaction_type = reaction_type
        reaction.save()
    else:
        reaction.reaction_type = reaction_type

    return JsonResponse({
        "like_count": experience.like_count,
        "dislike_count": experience.dislike_count,
    })


@login_required
def add_comment(request, experience_id):
    experience = get_object_or_404(TravelExperience, id=experience_id)

    if request.method == "POST":
        comment_text = request.POST.get("comment")
        if comment_text:
            Comment.objects.create(user=request.user, experience=experience, text=comment_text)

    return redirect("user_forum")

@login_required
def delete_experience(request, experience_id):
    experience = get_object_or_404(TravelExperience, id=experience_id)

    if request.user != experience.user:
        return HttpResponseForbidden("You are not allowed to delete this experience.")

    if request.method == "POST":
        experience.delete()
        return redirect("user_forum")

    return render(request, "profile/confirm_delete.html", {"experience": experience})

@login_required
def delete_account(request):
    if request.method == "POST":
        # Delete the user account
        user = request.user
        user.delete()
        # Log out the user after deleting the account
        logout(request)
        # Redirect to a confirmation page or the home page
        return redirect('account_deleted_confirmation')

    return render(request, 'profile/delete_account.html')

def account_deleted_confirmation(request):
    return render(request, 'profile/account_deleted_confirmation.html')


