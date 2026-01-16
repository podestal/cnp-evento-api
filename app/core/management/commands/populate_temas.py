"""
Django management command to populate Tema model with initial data.
"""
from django.core.management.base import BaseCommand
from storefront.models import Tema


class Command(BaseCommand):
    help = 'Populate Tema model with initial temas'

    def handle(self, *args, **options):
        temas_data = [
            {
                'title': 'Tema 1',
                'description': 'Regularización de firmas en los protocolos de notarios cesados',
                'coordinator': 'Notario Arturo Poma Rodrigo',
                'coordinator_celphone': '997448339',
            },
            {
                'title': 'Tema 2',
                'description': 'Cambio de nombre y rectificación de partidas en vía notarial',
                'coordinator': 'Notaria Jessie Tarcila Zegarra Cabrera',
                'coordinator_celphone': '995173232',
            },
            {
                'title': 'Tema 3',
                'description': 'Autorización notarial para disponer bienes de menores',
                'coordinator': 'Notario Reynaldo Pandia Mendoza',
                'coordinator_celphone': '985515436',
            },
            {
                'title': 'Tema 4',
                'description': 'Inclusión de Heredero preterido en sucesión intestada',
                'coordinator': 'Notario Marco Zuluaga Guerra',
                'coordinator_celphone': '951904081',
            },
            {
                'title': 'Tema 5',
                'description': 'Ofrecimiento de pago y consignación',
                'coordinator': 'Notario Israel Rubín de Celis Atencio',
                'coordinator_celphone': '964880809',
            },
        ]

        created_count = 0
        updated_count = 0

        for tema_data in temas_data:
            tema, created = Tema.objects.update_or_create(
                title=tema_data['title'],
                defaults={
                    'description': tema_data['description'],
                    'coordinator': tema_data['coordinator'],
                    'coordinator_celphone': tema_data['coordinator_celphone'],
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {tema.title}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Updated: {tema.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created: {created_count}, Updated: {updated_count}'
            )
        )
