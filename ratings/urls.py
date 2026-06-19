from django.urls import path
from .views import CreateRatingView, RiderRatingsView, MyRatingsView

urlpatterns = [
    path('job/<uuid:job_id>/',       CreateRatingView.as_view(),  name='create-rating'),
    path('rider/<uuid:rider_id>/',   RiderRatingsView.as_view(),  name='rider-ratings'),
    path('me/',                      MyRatingsView.as_view(),      name='my-ratings'),
]