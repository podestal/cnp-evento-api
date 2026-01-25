"""
Django management command to populate Activity model with initial data.
"""
from django.core.management.base import BaseCommand
from storefront.models import Activity
from datetime import date, time


class Command(BaseCommand):
    help = 'Populate Activity model with initial activities'

    def handle(self, *args, **options):
        # Activities for February 5-7, 2026
        activities_data = [
            # Jueves 05 de Febrero (Thursday, February 5th)
            {
                'name': 'Visita al complejo arqueológico de Sillustani',
                'day': date(2026, 2, 5),
                'time': time(13, 0),  # 13:00 h
                'is_active': True,
            },
            {
                'name': 'Conversatorio sobre "Jurisdicción Voluntaria"',
                'day': date(2026, 2, 5),
                'time': time(18, 0),  # 18:00 h
                'is_active': True,
            },
            {
                'name': 'Cóctel de bienvenida',
                'day': date(2026, 2, 5),
                'time': time(19, 0),  # 19:00 h
                'is_active': True,
            },
            # Viernes 06 de Febrero (Friday, February 6th)
            {
                'name': 'Registro de participantes',
                'day': date(2026, 2, 6),
                'time': time(8, 0),  # 8:00 h
                'is_active': True,
            },
            {
                'name': 'Ceremonia de inauguración con programa especial',
                'day': date(2026, 2, 6),
                'time': time(8, 30),  # 8:30 h
                'is_active': True,
            },
            {
                'name': 'Actividad académica',
                'day': date(2026, 2, 6),
                'time': time(9, 30),  # 9:30 h
                'is_active': True,
            },
            {
                'name': 'Almuerzo libre',
                'day': date(2026, 2, 6),
                'time': time(13, 0),  # 13:00 h
                'is_active': True,
            },
            {
                'name': 'Actividad académica',
                'day': date(2026, 2, 6),
                'time': time(15, 30),  # 15:30 h
                'is_active': True,
            },
            {
                'name': 'Cierre de actividades',
                'day': date(2026, 2, 6),
                'time': time(19, 20),  # 19:20 h
                'is_active': True,
            },
            # Sábado 07 de Febrero (Saturday, February 7th)
            {
                'name': 'Actividad Académica',
                'day': date(2026, 2, 7),
                'time': time(9, 0),  # 9:00 h
                'is_active': True,
            },
            {
                'name': 'Trabajo de comisiones',
                'day': date(2026, 2, 7),
                'time': time(9, 50),  # 9:50 h
                'is_active': True,
            },
            {
                'name': 'Debate y conclusiones',
                'day': date(2026, 2, 7),
                'time': time(10, 50),  # 10:50 h
                'is_active': True,
            },
            {
                'name': 'Clausura',
                'day': date(2026, 2, 7),
                'time': time(12, 0),  # 12:00 h
                'is_active': True,
            },
            {
                'name': 'Cena de gala y show costumbrista',
                'day': date(2026, 2, 7),
                'time': time(19, 0),  # 19:00 h
                'is_active': True,
            },
        ]

        created_count = 0
        updated_count = 0

        for activity_data in activities_data:
            # Use name, day, and time as unique identifier
            activity, created = Activity.objects.update_or_create(
                name=activity_data['name'],
                day=activity_data['day'],
                time=activity_data['time'],
                defaults={
                    'is_active': activity_data['is_active'],
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created: {activity.name} - {activity.day} {activity.time}'
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'↻ Updated: {activity.name} - {activity.day} {activity.time}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created: {created_count}, Updated: {updated_count}'
            )
        )
