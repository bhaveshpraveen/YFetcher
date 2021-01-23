from django.core.management.base import BaseCommand

from feed.utils.modelhelpers.apikeyhelper import APIKeyHelper


class Command(BaseCommand):
    """python manage.py runprerequisitescripts"""
    help = 'Run pre-requisite scripts here'

    def handle(self, *args, **options):
        APIKeyHelper.add_keys()
        self.stdout.write(self.style.SUCCESS("Successfully added api keys"))
