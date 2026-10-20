from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создаёт базовые роли: Волонтёр, Жертвователь, Координатор'

    def handle(self, *args, **options):
        for role in ['Волонтёр', 'Жертвователь', 'Координатор']:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS('Создана роль: ' + role))
            else:
                self.stdout.write('Роль уже есть: ' + role)

        coord = Group.objects.get(name='Координатор')
        coord.permissions.set(Permission.objects.all())
        self.stdout.write(self.style.SUCCESS('Координатор получил все права'))
