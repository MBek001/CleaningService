from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login,logout

from accounts.forms import LoginForm, ContactForm
from accounts.models import User, UserProfile, Referral, Reffered


class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm-password')

        referral_code = request.GET.get('referral_code')

        print("Referral code>> ", referral_code)

        if not first_name:
            messages.error(request, "First name is required.")
            return redirect('/register')

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('/register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists")
            return redirect('/register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email already exists")
            return redirect('/register')

        is_first_user = not User.objects.exists()

        user = User.objects.create(
            first_name=first_name,
            username=username,
            email=email,
            password=make_password(password1),
            is_superuser=is_first_user,
            is_staff=is_first_user
        )
        user.save()
        login(request, user)

        if referral_code:
            try:
                referral = Referral.objects.get(referral_code=referral_code)
                referring_user = referral.user
                user_profile, created = UserProfile.objects.get_or_create(user=user)
                user_profile.referred_by = referring_user
                user_profile.save()
                print("Referring user>> ", referring_user)

                Reffered.objects.create(
                    user=user,
                    referred_by=referral
                )

                referrer_profile, created = UserProfile.objects.get_or_create(user=referral.user)
                referrer_profile.prize_inviting = (referrer_profile.prize_inviting or 0) + 2
                referrer_profile.save()

                user_profile.prize_inviting = (user_profile.prize_inviting or 0) + 1
                user_profile.save()

            except Referral.DoesNotExist:
                pass

        return redirect('/')


class LoginView(View):
    template = "login.html"
    context = {}

    def get(self, request):
        form = LoginForm()
        self.context.update({'form': form})
        return render(request, self.template, self.context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Username or password is wrong !")

        return redirect('/login')


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/login')



def home(request):
    return render(request, 'index.html',{'user': request.user})

def service(request):
    return render(request, 'service.html')

def about(request):
    return render(request, 'about.html')

def project(request):
    return render(request, 'project.html')


def blog(request):
    return render(request, 'blog.html')


def single(request):
    return render(request, 'single.html')

def profile(request):
    return render(request, 'profile.html')



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            subject = f"Kleaning Website Message from {contact_message.name}"
            message = (
                f"Name: {contact_message.name}\n"
                f"Email: {contact_message.email}\n"
                f"Subject: {contact_message.subject}\n\n"
                f"Message:\n{contact_message.message}"
            )
            admin_email = 'mmm857436@gmail.com'
            send_mail(subject, message, contact_message.email, [admin_email])

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    context = {
        'form': form
    }
    return render(request, 'contact.html', context)


