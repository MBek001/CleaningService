from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from .models import UserProfile as Profile


class EditProfileView(LoginRequiredMixin, View):
    template_name = 'profile.html'

    def get(self, request):
        user = request.user
        try:
            user_profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            user_profile = None
        context = {
            'name': user.first_name,
            'username': user.username,
            'email': user.email,
            'profile_picture': user_profile.profile_picture if user_profile and user_profile.profile_picture else None
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        photo = request.FILES.get('photo')

        if name:
            user.first_name = name
        if username:
            if not User.objects.filter(username=username).exclude(pk=user.pk).exists():
                user.username = username
            else:
                messages.error(request, "This username is already taken.")
                return redirect('profile')

        if email:
            if not User.objects.filter(email=email).exclude(pk=user.pk).exists():
                user.email = email
            else:
                messages.error(request, "This email is already taken.")
                return redirect('profile')

        if photo:
            user_profile = Profile.objects.get_or_create(user=user)[0]
            user_profile.profile_picture = photo
            user_profile.save()

        user.save()
        messages.success(request, "Your profile has been updated!")
        return redirect('profile')


@login_required
def delete_profile_picture(request):
    user = request.user
    try:
        user_profile = Profile.objects.get(user=user)
        if user_profile.profile_picture:
            user_profile.profile_picture.delete(save=False)
            user_profile.profile_picture = None
            user_profile.save()

            if user_profile.prize_inviting is None :
                user_profile.delete()

            messages.success(request, "Profile picture deleted successfully.")
        else:
            messages.info(request, "No profile picture to delete.")
    except Profile.DoesNotExist:
        messages.warning(request, "Profile does not exist.")

    return redirect('profile')