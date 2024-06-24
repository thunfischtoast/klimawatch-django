from django.core.management.base import BaseCommand, CommandError
from klimawatch_app.models import Kommune, ActionSource, ActionField, Action
import json
from pathlib import Path


class Command(BaseCommand):
    help = "Rewrites the actions data from the json data"

    def handle(self, *args, **options):
        for path in Path("data/").glob("**/actions.json"):
            site = path.parent.name

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            kommune = Kommune.objects.get(slug=site)

            for field, actions in data.items():

                actionfield = ActionField.objects.get_or_create(name=field)[0]

                for action in actions:
                    source = ActionSource.objects.get_or_create(name=action.get("Source"))[0]
                    Action.objects.get_or_create(
                        kommune=kommune,
                        source=source,
                        field=actionfield,
                        action=action.get("Description"),
                        title=action.get("Title"),
                        short_title=action.get("Short Title"),
                    )

                    self.stdout.write(
                        self.style.SUCCESS("Successfully wrote actions data")
                    )
