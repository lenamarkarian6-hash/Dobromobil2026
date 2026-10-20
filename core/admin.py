from django.contrib import admin
from .models import Direction, Shelter, Trip, Enrollment


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction', 'address', 'lat', 'lng')
    list_filter = ('direction',)


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'direction', 'shelter', 'date', 'status', 'seats_taken', 'seats_total')
    list_filter = ('direction', 'status')
    date_hierarchy = 'date'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'trip', 'created_at', 'hours')
    list_filter = ('trip__direction',)
