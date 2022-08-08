from django.urls import path

from . import views

app_name = "articles"

urlpatterns = (
    path("", views.PartyListView.as_view(), name="party_list"),
    # FIXME Setup slug URLS based on id and party name
    path("<int:pk>/", views.PartyDetailView.as_view(), name="party_detail"),
)
