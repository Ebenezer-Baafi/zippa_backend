from django.urls import path
from .views import (
    CreateJobView, JobListView, JobDetailView,
    JobStatusUpdateView, CustomerJobCancelView
)

urlpatterns = [
    path('',                CreateJobView.as_view(),      name='create-job'),
    path('list/',           JobListView.as_view(),         name='job-list'),
    path('<uuid:job_id>/',  JobDetailView.as_view(),       name='job-detail'),
    path('<uuid:job_id>/status/', JobStatusUpdateView.as_view(),  name='job-status-update'),
    path('<uuid:job_id>/cancel/', CustomerJobCancelView.as_view(), name='job-cancel'),
]