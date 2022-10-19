from django.urls import path

from . import views


urlpatterns = [
    path('book_seat/<str:pk>', views.book_seat, name="book_seats"),
    path('booking_details', views.bookings, name="booking_details"),
    path('all_bookings', views.seebookings, name="all_bookings"),
    path('cancelling/<str:pk>', views.cancellings, name='cancelling')
]
