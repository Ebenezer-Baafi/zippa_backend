from django.urls import path
from .views import NegotiationCreateView, NegotiationListView, NegotiationResponseView

urlpatterns = [
    path('<uuid:job_id>/',               NegotiationCreateView.as_view(),  name='negotiation-create'),
    path('<uuid:job_id>/list/',          NegotiationListView.as_view(),    name='negotiation-list'),
    path('respond/<uuid:negotiation_id>/', NegotiationResponseView.as_view(), name='negotiation-respond'),
]