from django import forms

from .models import (
    ShelterApplication,
    Review,
    FAQQuestion
)


class ShelterApplicationForm(forms.ModelForm):
    """Форма подачи заявки на регистрацию приюта."""

    class Meta:
        model = ShelterApplication

        fields = [
            'direction',
            'shelter_name',
            'address',
            'lat',
            'lng',
            'contact_person',
            'contact_role',
            'email',
            'phone',
            'inn',
            'ogrn',
            'legal_status',
            'description',
            'animals_count',
            'operating_since',
            'needs',
            'photo1',
            'photo2',
            'photo3',
            'publication_consent',
        ]

        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Расскажите о вашем приюте'
            }),

            'needs': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Какая помощь вам сейчас необходима?'
            }),

            'operating_since': forms.TextInput(attrs={
                'placeholder': 'Например: с 2018 года'
            }),
        }


class ReviewForm(forms.ModelForm):
    """Форма отправки отзыва."""

    class Meta:
        model = Review

        fields = [
            'name',
            'role',
            'text',
            'rating',
        ]

        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Поделитесь впечатлениями о проекте'
            }),
        }


class FAQQuestionForm(forms.ModelForm):
    """Форма отправки вопроса посетителем."""

    class Meta:
        model = FAQQuestion

        fields = [
            'name',
            'email',
            'question',
        ]

        widgets = {
            'question': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишите ваш вопрос'
            }),
        }