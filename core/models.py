from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Direction(models.Model):
    """
    Направление помощи. Например: 'Помощь приютам животных',
    'Помощь бездомным', 'Экологический десант'.
    Сайт поддерживает несколько направлений — это ключевое требование ТЗ.
    """
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Слаг для URL', unique=True)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'
        ordering = ['name']

    def __str__(self):
        return self.name


class Shelter(models.Model):
    """
    Благополучатель: приют для животных или иная организация,
    которой помогает проект. Привязан к направлению.
    """
    direction = models.ForeignKey(
        Direction,
        on_delete=models.CASCADE,
        related_name='shelters',
        verbose_name='Направление'
    )
    name = models.CharField('Название', max_length=200)
    address = models.CharField('Адрес', max_length=300, blank=True)
    lat = models.FloatField('Широта', null=True, blank=True)
    lng = models.FloatField('Долгота', null=True, blank=True)
    needs = models.TextField('Потребности', blank=True)
    contact = models.CharField('Контакт', max_length=200, blank=True)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Приют'
        verbose_name_plural = 'Приюты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Trip(models.Model):
    """
    Рейс — конкретный выезд волонтёров/перевозчиков к приюту.
    Это единица координации: волонтёр записывается на рейс,
    координатор видит, кто едет, сколько мест осталось.
    """
    STATUS_PLANNED = 'planned'
    STATUS_OPEN = 'open'
    STATUS_FULL = 'full'
    STATUS_DONE = 'done'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PLANNED, 'Запланирован'),
        (STATUS_OPEN, 'Набор волонтёров'),
        (STATUS_FULL, 'Набран'),
        (STATUS_DONE, 'Выполнен'),
        (STATUS_CANCELLED, 'Отменён'),
    ]

    direction = models.ForeignKey(
        Direction,
        on_delete=models.CASCADE,
        related_name='trips',
        verbose_name='Направление'
    )
    shelter = models.ForeignKey(
        Shelter,
        on_delete=models.CASCADE,
        related_name='trips',
        verbose_name='Приют'
    )
    title = models.CharField('Название рейса', max_length=200)
    date = models.DateTimeField('Дата и время')
    seats_total = models.PositiveIntegerField('Всего мест', default=5)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PLANNED
    )
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'
        ordering = ['date']

    def seats_taken(self):
        """Сколько мест уже занято (по числу записей)."""
        return self.enrollments.count()

    def seats_left(self):
        """Сколько мест осталось. Не уходит в минус."""
        return max(0, self.seats_total - self.seats_taken())

    def is_open(self):
        """Можно ли ещё записаться."""
        return self.status == self.STATUS_OPEN and self.seats_left() > 0

    def __str__(self):
        return f'{self.title} — {self.date:%d.%m.%Y %H:%M}'


class Enrollment(models.Model):
    """
    Запись волонтёра на рейс. Один пользователь — одна запись на рейс
    (защита от дублей через unique_together). Часы заполняет координатор
    после выполнения рейса — из них складывается учёт часов волонтёра.
    """
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Рейс'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Волонтёр'
    )
    created_at = models.DateTimeField('Записался', auto_now_add=True)
    hours = models.PositiveIntegerField('Часы', default=0)
    is_attended = models.BooleanField('Посетил рейс', default=False)

    class Meta:
        verbose_name = 'Запись на рейс'
        verbose_name_plural = 'Записи на рейсы'
        unique_together = ('trip', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} → {self.trip.title}'




class VolunteerStep(models.Model):
    """Шаги инструкции о том, как стать волонтёром."""

    number = models.PositiveSmallIntegerField(
        'Номер шага',
        unique=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(6)
        ]
    )

    title = models.CharField(
        'Название шага',
        max_length=200
    )

    description = models.TextField(
        'Описание шага'
    )

    class Meta:
        verbose_name = 'Шаг волонтёра'
        verbose_name_plural = 'Шаги волонтёра'
        ordering = ['number']

    def __str__(self):
        return f'{self.number}. {self.title}'


class ShelterApplication(models.Model):
    """Заявка организации на регистрацию в проекте."""

    STATUS_NEW = 'new'
    STATUS_REVIEW = 'review'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_REVIEW, 'На рассмотрении'),
        (STATUS_APPROVED, 'Одобрена'),
        (STATUS_REJECTED, 'Отклонена'),
    ]

    direction = models.ForeignKey(
        Direction,
        on_delete=models.PROTECT,
        related_name='applications',
        verbose_name='Направление помощи'
    )

    shelter_name = models.CharField(
        'Название приюта',
        max_length=200
    )

    address = models.CharField(
        'Адрес',
        max_length=300
    )

    lat = models.FloatField(
        'Широта',
        null=True,
        blank=True
    )

    lng = models.FloatField(
        'Долгота',
        null=True,
        blank=True
    )

    contact_person = models.CharField(
        'Контактное лицо',
        max_length=200
    )

    contact_role = models.CharField(
        'Должность контактного лица',
        max_length=150,
        blank=True
    )

    email = models.EmailField(
        'Электронная почта'
    )

    phone = models.CharField(
        'Телефон',
        max_length=30
    )

    inn = models.CharField(
        'ИНН',
        max_length=12,
        blank=True
    )

    ogrn = models.CharField(
        'ОГРН',
        max_length=15,
        blank=True
    )

    legal_status = models.CharField(
        'Юридический статус',
        max_length=200,
        blank=True
    )

    description = models.TextField(
        'Описание приюта'
    )

    animals_count = models.PositiveIntegerField(
        'Количество животных',
        null=True,
        blank=True
    )

    operating_since = models.CharField(
        'Как давно работает приют',
        max_length=100,
        blank=True
    )

    needs = models.TextField(
        'Текущие потребности'
    )

    photo1 = models.ImageField(
        'Фотография 1',
        upload_to='shelter_applications/',
        blank=True,
        null=True
    )

    photo2 = models.ImageField(
        'Фотография 2',
        upload_to='shelter_applications/',
        blank=True,
        null=True
    )

    photo3 = models.ImageField(
        'Фотография 3',
        upload_to='shelter_applications/',
        blank=True,
        null=True
    )

    publication_consent = models.BooleanField(
        'Согласие на публикацию',
        default=False
    )

    status = models.CharField(
        'Статус заявки',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )

    created_at = models.DateTimeField(
        'Дата отправки',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Заявка приюта'
        verbose_name_plural = 'Заявки приютов'
        ordering = ['-created_at']

    def __str__(self):
        return self.shelter_name


class FAQ(models.Model):
    """Готовые вопросы и ответы для раздела FAQ."""

    question = models.CharField(
        'Вопрос',
        max_length=500
    )

    answer = models.TextField(
        'Ответ'
    )

    is_published = models.BooleanField(
        'Опубликован',
        default=True
    )

    order = models.PositiveIntegerField(
        'Порядок отображения',
        default=0
    )

    class Meta:
        verbose_name = 'Вопрос и ответ'
        verbose_name_plural = 'Часто задаваемые вопросы'
        ordering = ['order']

    def __str__(self):
        return self.question


class FAQQuestion(models.Model):
    """Вопрос, отправленный посетителем сайта."""

    name = models.CharField(
        'Имя',
        max_length=150
    )

    email = models.EmailField(
        'Электронная почта'
    )

    question = models.TextField(
        'Текст вопроса'
    )

    answer = models.TextField(
        'Ответ',
        blank=True
    )

    is_answered = models.BooleanField(
        'Получен ответ',
        default=False
    )

    created_at = models.DateTimeField(
        'Дата отправки',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Вопрос пользователя'
        verbose_name_plural = 'Вопросы пользователей'
        ordering = ['-created_at']

    def __str__(self):
        return f'Вопрос от {self.name}'


class Review(models.Model):
    """Отзыв о работе проекта."""

    ROLE_VOLUNTEER = 'volunteer'
    ROLE_SHELTER = 'shelter'
    ROLE_DRIVER = 'driver'
    ROLE_DONOR = 'donor'

    ROLE_CHOICES = [
        (ROLE_VOLUNTEER, 'Волонтёр'),
        (ROLE_SHELTER, 'Представитель приюта'),
        (ROLE_DRIVER, 'Водитель'),
        (ROLE_DONOR, 'Донор'),
    ]

    name = models.CharField(
        'Имя автора',
        max_length=150
    )

    role = models.CharField(
        'Роль автора',
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_VOLUNTEER
    )

    text = models.TextField(
        'Текст отзыва'
    )

    rating = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    is_published = models.BooleanField(
        'Опубликован',
        default=False
    )

    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.rating}/5'


class DonationReport(models.Model):
    """Отчёт о сборе и расходовании средств."""

    title = models.CharField(
        'Название отчёта',
        max_length=200
    )

    description = models.TextField(
        'Описание отчёта'
    )

    recipient = models.CharField(
        'Получатель помощи',
        max_length=200
    )

    target_amount = models.DecimalField(
        'Планируемая сумма',
        max_digits=12,
        decimal_places=2,
        default=0
    )

    collected_amount = models.DecimalField(
        'Собранная сумма',
        max_digits=12,
        decimal_places=2,
        default=0
    )

    spent_amount = models.DecimalField(
        'Потраченная сумма',
        max_digits=12,
        decimal_places=2,
        default=0
    )

    report_date = models.DateField(
        'Дата отчёта'
    )

    proof_url = models.URLField(
        'Ссылка на подтверждающие материалы',
        blank=True
    )

    is_published = models.BooleanField(
        'Опубликован',
        default=False
    )

    created_at = models.DateTimeField(
        'Дата создания записи',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отчёт о пожертвованиях'
        verbose_name_plural = 'Отчёты о пожертвованиях'
        ordering = ['-report_date']

    def __str__(self):
        return self.title


class AboutPage(models.Model):
    """Информация о проекте для страницы «О нас»."""

    title = models.CharField(
        'Заголовок',
        max_length=200,
        default='О проекте'
    )

    text = models.TextField(
        'Текст страницы'
    )

    photo = models.ImageField(
        'Фотография',
        upload_to='about/',
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(
        'Последнее обновление',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Страница о проекте'
        verbose_name_plural = 'Страница о проекте'

    def __str__(self):
        return self.title
