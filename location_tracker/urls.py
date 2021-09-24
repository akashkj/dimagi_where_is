from django.urls import path

from .views import LocationTrackerFormView, LocationQueryView

urlpatterns = [
    path('new/', LocationTrackerFormView.as_view(), name='post_new'),
    path('search/', LocationQueryView.as_view(), name='post_new'),
]
