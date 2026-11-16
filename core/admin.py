from django.contrib import admin

from .models import (
    Direction,
    Shelter,
    Trip,
    Enrollment,
    VolunteerStep,
    ShelterApplication,
    FAQ,
    FAQQuestion,
    Review,
    DonationReport,
    AboutPage,
)


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
    list_display = (
        'title',
        'direction',
        'shelter',
        'date',
        'status',
        'seats_taken',
        'seats_total',
    )
    list_filter = ('direction', 'status')
    date_hierarchy = 'date'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'trip', 'created_at', 'hours')
    list_filter = ('trip__direction',)


@admin.register(VolunteerStep)
class VolunteerStepAdmin(admin.ModelAdmin):
    list_display = ('number', 'title')
    ordering = ('number',)


@admin.register(ShelterApplication)
class ShelterApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'shelter_name',
        'direction',
        'contact_person',
        'phone',
        'status',
        'created_at',
    )

    list_filter = ('status', 'direction', 'created_at')

    search_fields = (
        'shelter_name',
        'contact_person',
        'email',
        'phone',
        'address',
    )

    readonly_fields = ('created_at',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_published', 'order')
    list_filter = ('is_published',)
    search_fields = ('question', 'answer')
    ordering = ('order',)


@admin.register(FAQQuestion)
class FAQQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'is_answered',
        'created_at',
    )

    list_filter = ('is_answered', 'created_at')
    search_fields = ('name', 'email', 'question')
    readonly_fields = ('created_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'role',
        'rating',
        'is_published',
        'created_at',
    )

    list_filter = ('role', 'rating', 'is_published')
    search_fields = ('name', 'text')
    readonly_fields = ('created_at',)


@admin.register(DonationReport)
class DonationReportAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'recipient',
        'target_amount',
        'collected_amount',
        'spent_amount',
        'report_date',
        'is_published',
    )

    list_filter = ('is_published', 'report_date')
    search_fields = ('title', 'recipient')
    readonly_fields = ('created_at',)


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    readonly_fields = ('updated_at',)