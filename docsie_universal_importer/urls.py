from django.urls import path

from .views import RepoMapView

urlpatterns = [
    path('repo_map/', RepoMapView.as_view(), name='repo_map'),
]
