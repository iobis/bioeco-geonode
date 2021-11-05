from django.core.management.base import BaseCommand, CommandError
from goos.models import EovResource


class Command(BaseCommand):
    help = "Populate GOOS specific fields"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
