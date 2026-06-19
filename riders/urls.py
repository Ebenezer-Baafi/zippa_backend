from django.urls import path
from .views import RiderProfileView, RiderAvailabilityView, RiderLocationView, NearbyRidersView

urlpatterns = [
    path('profile/',      RiderProfileView.as_view(),      name='rider-profile'),
    path('availability/', RiderAvailabilityView.as_view(), name='rider-availability'),
    path('location/',     RiderLocationView.as_view(),     name='rider-location'),
    path('nearby/',       NearbyRidersView.as_view(),      name='nearby-riders'),
]