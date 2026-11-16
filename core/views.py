from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Direction, Shelter, Trip, Enrollment, AboutPage

def home(request):
    directions = Direction.objects.filter(is_active=True)
    return render(request, 'core/home.html', {'directions': directions})

def about(request):
    about_page = AboutPage.objects.first()
    return render(request, 'core/about.html', {
        'about_page': about_page,
    })
def direction_detail(request, slug):
    direction = get_object_or_404(Direction, slug=slug, is_active=True)
    shelters = direction.shelters.all()
    trips = direction.trips.exclude(status='done')
    return render(request, 'core/direction_detail.html', {
        'direction': direction,
        'shelters': shelters,
        'trips': trips,
    })


def map_view(request):
    shelters = Shelter.objects.exclude(lat__isnull=True).exclude(lng__isnull=True)
    return render(request, 'core/map.html', {'shelters': shelters})


def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    return render(request, 'core/trip_detail.html', {'trip': trip})


@login_required
def enroll(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if trip.seats_left() <= 0:
        messages.error(request, 'Мест нет')
    elif Enrollment.objects.filter(trip=trip, user=request.user).exists():
        messages.warning(request, 'Вы уже записаны')
    else:
        Enrollment.objects.create(trip=trip, user=request.user)
        messages.success(request, 'Вы записались на рейс')
    return redirect('trip_detail', trip_id=trip.id)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})


@login_required
def cabinet(request):
    enrollments = request.user.enrollments.select_related('trip', 'trip__shelter').all()
    total_hours = sum(e.hours for e in enrollments)
    return render(request, 'core/cabinet.html', {
        'enrollments': enrollments,
        'total_hours': total_hours,
    })


def reports(request):
    directions = Direction.objects.filter(is_active=True)
    data = []
    for d in directions:
        data.append({
            'direction': d,
            'shelters': d.shelters.count(),
            'trips': d.trips.count(),
            'done_trips': d.trips.filter(status='done').count(),
            'volunteers': Enrollment.objects.filter(trip__direction=d).values('user').distinct().count(),
        })
    return render(request, 'core/reports.html', {'data': data})
