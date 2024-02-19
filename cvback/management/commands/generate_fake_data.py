from django.core.management.base import BaseCommand
from cvback.management.commands.fake_data import main

class Command(BaseCommand):
    help = 'Generates fake data for the application'

    def handle(self, *args, **options):        
        main()
        self.stdout.write(self.style.SUCCESS('Successfully generated fake data'))