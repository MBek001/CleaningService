from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .referral import ReferralView
from .views import RegisterView, LogoutView, LoginView
from accounts.profile_view import EditProfileView, delete_profile_picture

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('service/', views.service, name='service'),
    path('about/',views.about, name='about'),
    path('project/', views.project, name='project'),
    path('contact/', views.contact_view, name='contact'),
    path('profile/', EditProfileView.as_view(), name='profile'),
    path('blog/', views.blog, name='blog'),
    path('single/', views.single, name='single'),
    path('delete-profile-picture/', delete_profile_picture, name='delete_profile_picture'),
    path('referral/', ReferralView.as_view(), name='referral')

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

