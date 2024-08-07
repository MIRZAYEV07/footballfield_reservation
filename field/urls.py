from django.urls import path, include
from .views import FootballFieldListCreateView, FootballFieldDetailView, ReservationListCreateView, \
    ReservationDetailView, UserStatsView, FieldOwnerStatsView, ReviewCreateView

urlpatterns = [

    path('fields/', FootballFieldListCreateView.as_view(), name='field-list'),
    path('fields/<int:pk>/', FootballFieldDetailView.as_view(), name='field-detail'),
    path('reservations/', ReservationListCreateView.as_view(), name='reservation-list'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),
    path('user-stats/', UserStatsView.as_view(), name='user-stats'),
    path('owner-stats/', FieldOwnerStatsView.as_view(), name='owner-stats'),
    path('reviews/', ReviewCreateView.as_view(), name='review-create'),

]