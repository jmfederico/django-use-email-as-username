"""Define create_emailuser_app command."""

import os

from django.core.management import call_command
from django.core.management.templates import BaseCommand


class Command(BaseCommand):
    """Define create_emailuser_app command."""

    requires_system_checks = []
    help = (
        "Creates a Django app with a custom User model that subclasses the"
        " User model declared by Django Use Email as Username."
    )

    def add_arguments(self, parser):
        """Define arguments for create_emailuser_app command."""
        parser.add_argument(
            "name",
            nargs="?",
            default="custom_user",
            help="Optional name of the application or project. [custom_user]",
        )
        parser.add_argument(
            "directory", nargs="?", help="Optional destination directory"
        )

    def handle(self, name, **options):
        """Call "startapp" to generate app with custom user model."""
        options["template"] = (
            os.path.dirname(os.path.abspath(__file__)) + "/app_template"
        )
        try:
            del options["skip_checks"]
        except KeyError:
            pass
        call_command("startapp", name, **options)
