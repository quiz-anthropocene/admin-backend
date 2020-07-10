import yaml

from django.apps import apps
from django.core import serializers
from django.core.management.base import CommandError
from django.core.management.commands.dumpdata import Command as Dumpdata


class Command(Dumpdata):
    """
    https://docs.djangoproject.com/en/3.0/ref/django-admin/#dumpdata
    https://github.com/django/django/blob/master/django/core/management/commands/dumpdata.py

    Custom --pretty argument (old)
    Get readable data in the dumpdata output https://djangosnippets.org/snippets/10625/

    Usage example:
    python manage.py dumpdata api.question > data/questions.yaml
    python manage.py dumpdata api.question --format=yaml --output=data/questions.yaml
    python manage.py dumpdata api.question --format=yaml-pretty --output=data/questions.yaml
    python manage.py dumpdata api.question --format=yaml-pretty-flat --output=data/questions.yaml
    """

    def handle(self, *app_labels, **options):
        # pretty: allow_unicode to have a clean and readable output
        # flat: output with 'model', 'pk' and 'fields' keys
        if options.get("format").startswith("yaml-"):
            # init
            if (len(app_labels) == 0) or (len(app_labels) > 1):
                raise CommandError("error with app_labels. only 1 'app.model' possible")
            else:
                app_label, model_label = app_labels[0].split(".")
                model = apps.get_app_config(app_label).get_model(model_label)
            output = options["output"]
            stream = open(output, "w") if output else None
            # yaml + pretty : call django serializer
            if options.get("format") == "yaml-pretty":
                model_queryset = model.objects.all()
                serializers.serialize(
                    "yaml",
                    model_queryset,
                    stream=stream or self.stdout,
                    allow_unicode=True,
                )
            # yaml + pretty + flat : call pyyaml
            elif options.get("format") == "yaml-pretty-flat":
                model_queryset_values_list = list(model.objects.values())
                yaml.safe_dump(
                    model_queryset_values_list,
                    stream=stream or self.stdout,
                    allow_unicode=True,
                    sort_keys=False,
                )
        else:
            super(Command, self).handle(*app_labels, **options)
