from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import View
from .models import Referral, Reffered as Referred
from .utils import generate_unique_code


@method_decorator(login_required, name='dispatch')
class ReferralView(View):
    template_name = 'referral.html'

    def get(self, request):
        user = request.user

        try:
            referral = Referral.objects.get(user=user)
            referral_link = request.build_absolute_uri(f'/register/?referral_code={referral.referral_code}')
        except Referral.DoesNotExist:
            referral_link = None
        except Referral.MultipleObjectsReturned:
            referral_link = "Error: Multiple referral entries found."

        referred_users = Referred.objects.filter(referred_by__user=user)

        context = {
            'referral_link': referral_link,
            'referred_users': referred_users
        }

        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user

        if Referral.objects.filter(user=user).exists():
            messages.warning(request, "You already have a referral link.")
        else:
            referral_code = generate_unique_code()
            Referral.objects.create(user=user, referral_code=referral_code)
            referral_link = request.build_absolute_uri(f'/register/?referral_code={referral_code}')
            messages.success(request, f"Your referral link has been generated: {referral_link}")

        return redirect('referral')
