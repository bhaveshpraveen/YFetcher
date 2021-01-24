from aiocrontab import Crontab
from django.core.management.base import BaseCommand, CommandError

from feed.utils.videofetchinghelper import VideoFetchingHelper


class Command(BaseCommand):
    """python manage.py fetchvideos"""

    help = "Fetches Videos and creates entries in Video model"

    def add_arguments(self, parser):
        parser.add_argument("search_terms", nargs="+", type=str)

    def handle(self, *args, **options):
        aiocrontab = Crontab()
        self.stdout.write(self.style.SUCCESS(f"options: {options['search_terms']}"))

        for search_term in options["search_terms"]:
            helper = VideoFetchingHelper(search_term)
            aiocrontab.register("* * * * *")(helper.run)

        aiocrontab.run()
        self.stdout.write(self.style.SUCCESS())
