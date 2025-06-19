from django.urls import path
from .views import ProductClipper

urlpatterns = [
    path('', ProductClipper.as_view()),
]