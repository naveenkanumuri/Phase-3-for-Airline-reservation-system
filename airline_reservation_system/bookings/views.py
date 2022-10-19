from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Booking, Flight


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'bookings/home_without_signin.html')
    username = request.user.username
    flights = Flight.objects.all()
    return render(request, 'bookings/home.html', {'flights': flights, 'username': username})


@login_required(login_url='signin')
def book_seat(request, pk):
    flight = Flight.objects.get(id=pk)
    return render(request, "bookings/book_seat.html", {'flight': flight})


@login_required(login_url='signin')
def bookings(request):
    if request.method != 'POST':
        return render(request, 'bookings/booking_details.html')
    print(request.POST.get('flight_id'))
    flight_id = request.POST.get('flight_id')
    no_of_seats = int(request.POST.get('no_seats'))
    if flight := Flight.objects.get(id=flight_id):
        if flight.remaining_seats >= no_of_seats:
            one_seat_price = flight.price
            total_price = no_of_seats * one_seat_price
            remaining_update = flight.remaining_seats - no_of_seats
            Flight.objects.filter(id=flight_id).update(remaining_seats=remaining_update)

            book = Booking.objects.create(name=request.user.username,
                                          email=request.user.email,
                                          user_id=request.user.id,
                                          flight_name=flight.flight_name,
                                          source=flight.source,
                                          flight_id=flight_id,
                                          destination=flight.destination,
                                          price=total_price,
                                          no_of_seats=no_of_seats,
                                          date=flight.date,
                                          time=flight.time,
                                          status='BOOKED'
                                        )
            book.save()
            messages.success(request, 'Booking Confirmed')
            return render(request, 'bookings/booking_details.html', locals())
        else:
            messages.error(request, 'No Seats available')
            return redirect('home')


@login_required(login_url='signin')
def seebookings(request):
    user_id = request.user.id
    if bookings := Booking.objects.filter(user_id=user_id):
        return render(request, 'bookings/bookings.html', locals())
    else:
        return redirect('home')


@login_required(login_url='signin')
def cancellings(request, pk):
    if request.method == 'POST':
        book = Booking.objects.get(id=pk)
        flight = Flight.objects.get(id=book.flight_id)
        remaining_update = flight.remaining_seats + book.no_of_seats
        Flight.objects.filter(id=book.flight_id).update(remaining_seats=remaining_update)
        Booking.objects.filter(id=pk).update(status='CANCELLED')
        Booking.objects.filter(id=pk).update(no_of_seats=0)
        messages.error(request, "Booking has been cancelled successfully")
        return redirect('all_bookings')
    else:
        return redirect('home')
