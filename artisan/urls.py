"""
URL configuration for artisan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.views import SignUp, DashboardArtisans, Artisan_Login, AddCraft, UpdateArtisanProfile, ArtisanAddPaymentAccount, ArtisanUpdateAccount, logoutArtisan, Buyer_Login, BuyerDashboard, ConfirmAddToCart, MakePayment, ConfirmPayment, logoutBuyer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("app.urls")),
    path('register/', SignUp.as_view(), name='register'),
    path('artisans/', DashboardArtisans.as_view(), name='artisans'),
    path('artisan_login/', Artisan_Login.as_view(), name='artisan_login'),
    path('add_design/', AddCraft.as_view(), name='add_design'),
    path('artisan_update/<str:uuid>/', UpdateArtisanProfile.as_view(), name='artisan_update_profile'),
    path('add_account/', ArtisanAddPaymentAccount.as_view(), name='add_account'),
    path('add_account/', ArtisanUpdateAccount.as_view(), name='update_account'),
    path("logout/", logoutArtisan, name="logout"),
    path("logout__/", logoutBuyer, name="logout__"),
    path("buyer_login/", Buyer_Login.as_view(), name="buyer_login"),
    path("buyers/", BuyerDashboard.as_view(), name="buyers"),
    path("confirm/<str:uuid>/", ConfirmAddToCart.as_view(), name="confirm_add_cart"),
    path("payment/<str:uuid>/", MakePayment.as_view(), name="payment"),
    path("confirm_payment/<str:uuid>/", ConfirmPayment.as_view(), name="confirm_payment"),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
